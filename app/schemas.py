from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ApplicationCreate(BaseModel):
    company: str
    role: str
    job_description: Optional[str] = None
    notes: Optional[str] = None

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    job_description: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: str
    date_applied: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class ResumeResponse(BaseModel):
    id: int
    filename: str
    s3_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class MatchResultResponse(BaseModel):
    match_score: float
    analysis: str

class SkillGapResponse(BaseModel):
    missing_skills: str
    present_skills: str
    recommendations: str


class DashboardStats(BaseModel):
    total_applications: int
    applied: int
    interviews: int
    offers: int
    rejections: int
    interview_rate: float
    offer_rate: float