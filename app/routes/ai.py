from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application, Resume, MatchResult, SkillGap, User
from app.auth import get_current_user
from app.ai import get_match_score, get_skill_gap

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/match/{application_id}/{resume_id}")
def match_score(application_id: int, resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    result = get_match_score(resume.parsed_text, application.job_description)
    match = MatchResult(
        user_id=current_user.id,
        application_id=application_id,
        resume_id=resume_id,
        match_score=float(result.split("MATCH_SCORE:")[1].split("\n")[0].strip()),
        analysis=result.split("ANALYSIS:")[1].strip()
    )
    db.add(match)
    db.commit()
    return {"match_score": match.match_score, "analysis": match.analysis}


@router.post("/skillgap/{application_id}/{resume_id}")
def skill_gap(application_id: int, resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    result = get_skill_gap(resume.parsed_text, application.job_description)
    gap = SkillGap(
        user_id=current_user.id,
        application_id=application_id,
        resume_id=resume_id,
        present_skills=result.split("PRESENT_SKILLS:")[1].split("\n")[0].strip(),
        missing_skills=result.split("MISSING_SKILLS:")[1].split("\n")[0].strip(),
        recommendations=result.split("RECOMMENDATIONS:")[1].strip()
    )
    db.add(gap)
    db.commit()
    return {
        "present_skills": gap.present_skills,
        "missing_skills": gap.missing_skills,
        "recommendations": gap.recommendations
    }