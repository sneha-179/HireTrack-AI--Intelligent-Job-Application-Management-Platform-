# HireTrack AI

A backend API to manage your job applications intelligently.
Upload your resume, paste a job description, and let AI tell you
how well you match and what skills you're missing.

Built with FastAPI + MySQL + Google Gemini.

---

## What it does

- Add and track job applications (company, role, status, notes)
- Upload your resume as PDF
- Get AI-powered match score between your resume and a job description
- See skill gaps — what you have vs what the job needs
- Dashboard with stats (total applied, interviews, offers, rejections)

---

## Tech Stack

- **FastAPI** — REST API framework
- **MySQL + SQLAlchemy** — database and ORM
- **Google Gemini API** — AI match scoring and skill gap analysis
- **PyMuPDF** — PDF parsing
- **JWT + bcrypt** — authentication
- **AWS S3** — resume file storage
- **Docker** — containerization
- **Pytest** — automated testing

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/sneha-179/hiretrack-ai.git
cd hiretrack-ai
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup environment**
```bash
cp .env.example .env
# fill in your values in .env
```

**5. Create database**
```sql
CREATE DATABASE hiretrack;
```

**6. Run**
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` to see all endpoints.

---

## API Endpoints

**Auth**
- `POST /auth/register` — create account
- `POST /auth/login` — get JWT token
- `GET /auth/logout` — logout
- `GET /auth/me` — get your profile

**Applications**
- `POST /applications/` — add new application
- `GET /applications/` — get all your applications
- `GET /applications/{id}` — get one application
- `PUT /applications/{id}` — update application
- `DELETE /applications/{id}` — delete application
- `GET /applications/filter?status=Interview` — filter by status

**Resume**
- `POST /resumes/upload` — upload PDF resume
- `GET /resumes/` — get your resume
- `DELETE /resumes/{id}` — delete resume

**AI**
- `POST /ai/match/{application_id}/{resume_id}` — get match score
- `POST /ai/skillgap/{application_id}/{resume_id}` — get skill gaps

**Dashboard**
- `GET /dashboard/stats` — your application stats
- `GET /dashboard/summary` — recent applications

**Users**
- `GET /users/profile` — get profile
- `PUT /users/profile` — update profile

---

## Testing

```bash
$env:PYTHONPATH = "."; pytest tests/ -v
```

22 test cases covering auth, applications, resume upload and AI endpoints.

---

## Future Scope

Gmail integration — connect your inbox, auto-detect company replies
and update application status automatically without manual tracking.