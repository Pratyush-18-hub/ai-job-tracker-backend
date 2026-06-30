import google.generativeai as genai
import os
import json
import re
import time
from dotenv import load_dotenv
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def call_gemini(prompt):
    for attempt in range(5):
        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            print(e)

            if "429" in str(e):
                msg = str(e)

                m = re.search(r"retry in ([0-9.]+)s", msg)

                if m:
                    wait = int(float(m.group(1))) + 2
                else:
                    wait = 30

                print(f"Waiting {wait} seconds before retrying...")
                time.sleep(wait)

            else:
                raise

    raise Exception("Gemini API failed after retries.")

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
        print("Resume characters:", len(text))
    return text

def analyze_resume(job_description: str, resume_text: str):
    prompt = f"""
You are an expert ATS (Applicant Tracking System) scanner.

Analyze this resume against the job description exactly like a real ATS system.
Respond ONLY in this exact JSON format. No markdown, no backticks, pure JSON only:

{{
  "ats_score": <number 0-100>,
  "keyword_match": <number 0-100>,
  "experience_match": <number 0-100>,
  "skills_match": <number 0-100>,
  "matched_keywords": ["keyword1", "keyword2", "keyword3"],
  "missing_keywords": ["keyword1", "keyword2", "keyword3"],
  "missing_skills": ["skill1", "skill2", "skill3"],
  "suggestions": ["suggestion1", "suggestion2", "suggestion3"],
  "summary": "honest one paragraph assessment"
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY the JSON. Nothing else.
"""
    print("Analyze Prompt Size:", len(prompt))
    response_text = call_gemini(prompt)
    clean = response_text.strip()
    clean = re.sub(r'```json|```', '', clean).strip()
    return json.loads(clean)

def improve_resume(job_description: str, resume_text: str, candidate_name: str):
    prompt = f"""
You are a world-class ATS resume optimization expert.

Rewrite the resume below to achieve maximum ATS score for the given job description.

STRICT RULES:
1. Never fabricate experience, education, or skills
2. Only add keywords that genuinely apply to existing experience
3. Use strong action verbs (Developed, Implemented, Architected, Optimized, Led)
4. Quantify achievements wherever possible (%, numbers, metrics)
5. Match exact keywords and phrases from the job description
6. Keep bullet points concise and impactful (one line each)
7. Use the EXACT format below — do not deviate

REQUIRED OUTPUT FORMAT (follow exactly):
---
{candidate_name}

[email] | [phone] | [location] | [github]

PROFESSIONAL SUMMARY
2-3 sentences matching candidate to this specific role using JD keywords

TECHNICAL SKILLS
Languages: [list relevant languages from resume, add any missing ones from JD if candidate knows them]
Frameworks & Libraries: [list relevant frameworks]
Databases: [list relevant databases]
Cloud & Tools: [list cloud and tools]
AI/ML: [list if applicable]

EDUCATION
[Degree] — [Specialization] | CGPA: [x.xx]/10
[University Name] | [Year Range]
Relevant Coursework: [list courses matching JD requirements]

EXPERIENCE
[Company Name] — [Role] | [Duration]
- [Strong action verb] + [what you did] + [impact/result with metrics if possible]
- [Strong action verb] + [what you did] + [impact/result with metrics if possible]
- [Strong action verb] + [what you did] + [impact/result with metrics if possible]

PROJECTS
[Project Name] | [Tech Stack]
- [Strong action verb] + [what you built] + [impact/metrics]
- [Strong action verb] + [technical detail matching JD keywords]
- [Strong action verb] + [result or achievement]

CERTIFICATIONS & ACHIEVEMENTS
- [Any relevant certifications or achievements]

AREAS OF INTEREST
[List interests matching JD focus areas]
---

JOB DESCRIPTION:
{job_description}

ORIGINAL RESUME:
{resume_text}

Output ONLY the resume content between the --- markers. Nothing else.
"""
    print("Improve Prompt Size:", len(prompt))
    text = call_gemini(prompt)
    text = text.strip()
    if '---' in text:
        parts = text.split('---')
        if len(parts) >= 3:
            text = parts[1].strip()
        elif len(parts) == 2:
            text = parts[1].strip()
    return text

def generate_pdf(resume_text: str, candidate_name: str):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch,
    )

    name_style = ParagraphStyle('Name', fontName='Helvetica-Bold',
                                 fontSize=17, spaceAfter=3,
                                 textColor=colors.HexColor('#0a3d62'))
    contact_style = ParagraphStyle('Contact', fontName='Helvetica',
                                    fontSize=9, spaceAfter=8,
                                    textColor=colors.HexColor('#444444'))
    heading_style = ParagraphStyle('Heading', fontName='Helvetica-Bold',
                                    fontSize=11, spaceBefore=10, spaceAfter=2,
                                    textColor=colors.HexColor('#0a3d62'))
    subheading_style = ParagraphStyle('SubHeading', fontName='Helvetica-Bold',
                                       fontSize=9.5, spaceAfter=1)
    bullet_style = ParagraphStyle('Bullet', fontName='Helvetica',
                                   fontSize=9, leftIndent=14,
                                   spaceAfter=2, leading=12)
    body_style = ParagraphStyle('Body', fontName='Helvetica',
                                 fontSize=9, spaceAfter=2, leading=12)
    skill_style = ParagraphStyle('Skill', fontName='Helvetica',
                                  fontSize=9, spaceAfter=2, leading=12)

    story = []
    lines = resume_text.split('\n')

    for i, line in enumerate(lines):
        line = line.strip()

        if not line:
            story.append(Spacer(1, 3))

        elif i == 0:
            story.append(Paragraph(line, name_style))

        elif '@' in line or '+91' in line or 'github' in line.lower():
            story.append(Paragraph(line, contact_style))
            story.append(HRFlowable(width="100%", thickness=1,
                                     color=colors.HexColor('#0a3d62'),
                                     spaceAfter=5))

        elif line.isupper():
            story.append(Paragraph(line, heading_style))
            story.append(HRFlowable(width="100%", thickness=0.4,
                                     color=colors.HexColor('#cccccc'),
                                     spaceAfter=3))

        elif line.startswith('- ') or line.startswith('• '):
            story.append(Paragraph('&bull; ' + line[2:], bullet_style))

        elif ':' in line and len(line.split(':')[0].split()) <= 4:
            parts = line.split(':', 1)
            formatted = f"<b>{parts[0]}:</b>{parts[1]}"
            story.append(Paragraph(formatted, skill_style))

        elif '|' in line and i > 2:
            story.append(Paragraph(line, subheading_style))

        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer