from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    job_description = Column(Text, nullable=True)
    status = Column(String(50), default="Applied")
    date_applied = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    s3_url = Column(String(500), nullable=False)
    parsed_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    missing_skills = Column(Text, nullable=False)
    present_skills = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)