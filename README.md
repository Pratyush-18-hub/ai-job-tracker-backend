# 💼 AI Job Tracker — Backend

The backend service for **AI Job Tracker**, a full-stack application for managing job applications and using AI to analyze job-related information.

The backend is built with **FastAPI** and provides REST APIs for the React frontend. It handles authentication, database operations, AI-powered analysis, and document processing.

## ✨ Features

* ⚡ REST API built with FastAPI
* 🔐 JWT-based user authentication
* 👤 User-specific application data
* 💼 Job application management
* 🤖 AI-powered job analysis
* 🗄️ PostgreSQL database integration
* 🔄 SQLAlchemy ORM
* 📄 PDF processing
* 📑 PDF generation
* 🔑 Secure password hashing
* 🌐 CORS/API communication with the frontend
* 🔒 Environment-based configuration

The repository contains dedicated modules for AI analysis, authentication, JWT handling, database configuration, models, and the FastAPI application.

## 🛠️ Tech Stack

### Backend

* **Python**
* **FastAPI**
* **Uvicorn**
* **SQLAlchemy**
* **PostgreSQL**
* **Psycopg2**
* **Google Generative AI**
* **JWT**
* **Passlib**
* **bcrypt**
* **python-dotenv**

### Document Processing

* **PyPDF**
* **ReportLab**
* **python-multipart**

These technologies are included in the project's backend dependencies.

## 🏗️ Architecture

The backend acts as the central application layer between the React frontend, database, and AI service.

```text id="6b5g9k"
                    React Frontend
                         │
                    HTTP Requests
                         │
                         ▼
                  ┌─────────────┐
                  │   FastAPI   │
                  │     API     │
                  └──────┬──────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
   Authentication    PostgreSQL     Google AI
          │              │              │
          ▼              ▼              ▼
       JWT/Auth       SQLAlchemy    AI Analysis
```

## 📂 Project Structure

```text id="a9p7cd"
ai-job-tracker-backend/
│
├── ai_analysis.py       # AI-powered analysis
├── auth.py              # Authentication utilities
├── auth_token.py        # JWT/token handling
├── database.py          # Database configuration
├── main.py              # FastAPI application and routes
├── models.py            # Database models
├── requirements.txt     # Python dependencies
└── .gitignore
```

The current repository contains these backend modules.

## 🤖 AI Analysis

The backend contains a dedicated:

```text
ai_analysis.py
```

module for AI-related processing.

Google Generative AI is used as part of the backend's AI functionality.

The AI layer is designed to analyze job-related information and provide useful insights to the application.

## 🔐 Authentication

Authentication is handled on the backend using dedicated modules:

```text
auth.py
auth_token.py
```

The authentication stack includes:

* JWT
* Passlib
* bcrypt
* `python-jose`

These provide the foundation for secure user authentication and password handling.

## 🗄️ Database

The application uses **PostgreSQL** as its relational database.

SQLAlchemy is used as the ORM layer:

```text id="b6r8p1"
FastAPI
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL
```

Database-related code is separated into:

```text id="t2p1i4"
database.py
models.py
```

## 📄 PDF & Document Processing

The backend includes document-processing capabilities using:

### PyPDF

Used for working with PDF documents.

### ReportLab

Used for generating PDF documents.

### python-multipart

Provides support for multipart form-data, which is useful when handling uploaded files.

These dependencies are included in `requirements.txt`.

## 🚀 Getting Started

### 1. Clone the repository

```bash id="5uh2t7"
git clone https://github.com/Pratyush-18-hub/ai-job-tracker-backend.git
```

Navigate into the project:

```bash id="5k2a4p"
cd ai-job-tracker-backend
```

### 2. Create a virtual environment

```bash id="l7txjg"
python -m venv .venv
```

### 3. Activate the environment

**Windows:**

```powershell id="g4m0n2"
.venv\Scripts\activate
```

### 4. Install dependencies

```bash id="c9t6jk"
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file in the backend project directory.

Example:

```env id="0t4r9j"
DATABASE_URL=your_postgresql_connection_string
GOOGLE_API_KEY=your_google_ai_api_key
SECRET_KEY=your_secret_key
```

Use the actual variable names expected by your backend configuration.

**Never commit `.env` or API keys to GitHub.**

## ▶️ Run the Backend

Start the FastAPI development server with:

```bash id="l2x1kf"
uvicorn main:app --reload
```

The API will normally be available at:

```text id="0qg7gc"
http://127.0.0.1:8000
```

FastAPI provides interactive API documentation at:

```text id="8k3q0v"
http://127.0.0.1:8000/docs
```

## 🔗 Frontend

The backend is designed to work with the separate React frontend.

### Frontend Repository

[AI Job Tracker — Frontend](https://github.com/Pratyush-18-hub/ai-job-tracker?utm_source=chatgpt.com)

The frontend communicates with this backend through HTTP API requests.

## 🔄 Request Flow

```text id="1omxgk"
User
 │
 ▼
React Frontend
 │
 │ Axios
 ▼
FastAPI Backend
 │
 ├── Authenticate User
 │
 ├── Process Request
 │
 ├── Query PostgreSQL
 │
 ├── Perform AI Analysis
 │
 └── Return Response
 │
 ▼
React Frontend
 │
 ▼
User
```

## 🌐 Deployment

The backend can be deployed independently from the frontend.

Example architecture:

```text id="5brt7s"
                  React Frontend
                        │
                        │ HTTPS
                        ▼
                  FastAPI Backend
                    /         \
                   /           \
                  ▼             ▼
            PostgreSQL       Google AI
```

This separation allows the frontend and backend to be developed, deployed, and maintained independently.

## 🧪 API Documentation

Once the backend is running, FastAPI automatically provides interactive API documentation:

```text id="7i5w4h"
http://127.0.0.1:8000/docs
```

This can be used to inspect and test available API endpoints.

## 🎯 Learning Outcomes

This backend project provided practical experience with:

* FastAPI development
* REST API design
* PostgreSQL
* SQLAlchemy ORM
* JWT authentication
* Password hashing
* Generative AI integration
* PDF processing
* Environment variables
* CORS and frontend/backend communication
* Backend deployment
* Full-stack application architecture

## 🔮 Future Improvements

Potential improvements include:

* [ ] More advanced AI job matching
* [ ] Resume-to-job compatibility scoring
* [ ] Automated job recommendations
* [ ] Job application reminders
* [ ] Email notification system
* [ ] More detailed analytics APIs
* [ ] Improved API validation
* [ ] Automated testing
* [ ] API rate limiting
* [ ] Better error handling and logging

## 👨‍💻 Author

**Pratyush Sahoo**

GitHub: [Pratyush-18-hub](https://github.com/Pratyush-18-hub?utm_source=chatgpt.com)

## 📄 License

This project is intended for educational and portfolio purposes.
