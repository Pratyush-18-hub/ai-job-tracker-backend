from fastapi import FastAPI, Depends,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ai_analysis import extract_text_from_pdf, analyze_resume, improve_resume, generate_pdf
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal, Base
from auth import hash_password,verify_password
from auth_token import create_token
 
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

@app.post("/jobs")
def add_job(job: dict, db: Session = Depends(get_db)):
    new_job = models.Job(
        company=job["company"],
        role=job["role"],
        status=job["status"]
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job
@app.post("/signup")
def signup(user: dict,db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user["email"]).first()
    if existing_user:
        return{"error":"Email already registered"}
    
    new_user = models.User(
        name = user["name"],
        email = user["email"],
        password = hash_password(user["password"])
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message":"signup successful"}

@app.post("/login")
def login(user: dict,db: Session=(Depends(get_db))):
    db_user = db.query(models.User).filter(models.User.email == user["email"]).first()
    if not db_user:
        return{"error":"User not found"}
    if not verify_password(user["password"],db_user.password):
        return{"error": "Incorrect password"}
        
    token = create_token({"user_id": db_user.id})
    return {"token" : token,"name": db_user.name}

@app.post("/analyze")
async def analyze(
    resume : UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume.file)
    analysis = analyze_resume(job_description,resume_text)
    return analysis
@app.post("/improve-resume")  
async def improve(
    resume : UploadFile = File(...),
    job_description: str = Form(...),
    candidate_name: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume.file)
    improved_text = improve_resume(job_description,resume_text,candidate_name)
    pdf_Buffer = generate_pdf(improved_text,candidate_name)
    return StreamingResponse(
        pdf_Buffer,
        media_type= "application/pdf",
        headers={"Content-Disposition":"attachment ; filename: improved_resume.pdf"}
    )
