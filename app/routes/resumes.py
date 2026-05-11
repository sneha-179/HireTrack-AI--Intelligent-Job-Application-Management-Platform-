from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Resume, User
from app.auth import get_current_user
from app.s3 import upload_resume, get_presigned_url, delete_resume
from app.ai import parse_resume
import uuid

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", status_code=201)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    file_bytes = await file.read()
    unique_filename = f"{current_user.id}_{uuid.uuid4()}_{file.filename}"
    s3_url = upload_resume(file_bytes, unique_filename)
    parsed_text = parse_resume(file_bytes)
    resume = Resume(
        user_id=current_user.id,
        filename=unique_filename,
        s3_url=s3_url,
        parsed_text=parsed_text
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return {"message": "Resume uploaded successfully", "resume_id": resume.id, "s3_url": s3_url}


@router.get("/")
def get_resume(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")
    presigned_url = get_presigned_url(resume.filename)
    return {"resume_id": resume.id, "filename": resume.filename, "presigned_url": presigned_url, "uploaded_at": resume.uploaded_at}


@router.delete("/{resume_id}")
def delete(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    delete_resume(resume.filename)
    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted successfully"}