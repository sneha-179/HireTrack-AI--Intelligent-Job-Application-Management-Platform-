from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import get_current_user, hash_password
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at
    }


@router.put("/profile")
def update_profile(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.name:
        current_user.name = data.name
    if data.password:
        current_user.password = hash_password(data.password)
    db.commit()
    db.refresh(current_user)
    return {"message": "Profile updated successfully"}