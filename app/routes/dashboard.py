from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application, User
from app.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    applications = db.query(Application).filter(Application.user_id == current_user.id).all()
    total = len(applications)
    applied = len([a for a in applications if a.status == "Applied"])
    interviews = len([a for a in applications if a.status == "Interview"])
    offers = len([a for a in applications if a.status == "Offer"])
    rejections = len([a for a in applications if a.status == "Rejected"])
    interview_rate = round((interviews / total) * 100, 2) if total > 0 else 0
    offer_rate = round((offers / total) * 100, 2) if total > 0 else 0
    return {
        "total_applications": total,
        "applied": applied,
        "interviews": interviews,
        "offers": offers,
        "rejections": rejections,
        "interview_rate": f"{interview_rate}%",
        "offer_rate": f"{offer_rate}%"
    }


@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).order_by(Application.date_applied.desc()).limit(5).all()
    return {
        "recent_applications": [
            {
                "company": a.company,
                "role": a.role,
                "status": a.status,
                "date_applied": a.date_applied
            } for a in applications
        ]
    }