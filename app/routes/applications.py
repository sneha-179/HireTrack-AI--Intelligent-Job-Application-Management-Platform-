from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application, User
from app.schemas import ApplicationCreate, ApplicationUpdate
from app.auth import get_current_user
from typing import Optional

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/", status_code=201)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = Application(
        user_id=current_user.id,
        company=data.company,
        role=data.role,
        job_description=data.job_description,
        notes=data.notes
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return {"message": "Application added successfully", "application_id": application.id}


@router.get("/")
def get_all_applications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    applications = db.query(Application).filter(Application.user_id == current_user.id).all()
    return applications


@router.get("/filter")
def filter_by_status(status: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Application).filter(Application.user_id == current_user.id)
    if status:
        query = query.filter(Application.status == status)
    return query.all()


@router.get("/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/{application_id}")
def update_application(application_id: int, data: ApplicationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if data.company: application.company = data.company
    if data.role: application.role = data.role
    if data.job_description: application.job_description = data.job_description
    if data.status: application.status = data.status
    if data.notes: application.notes = data.notes
    db.commit()
    db.refresh(application)
    return {"message": "Application updated successfully"}


@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return {"message": "Application deleted successfully"}