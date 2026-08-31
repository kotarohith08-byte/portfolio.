"""
StudyChart AI - Study Sessions API Endpoints.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.study_service import StudyService

router = APIRouter(prefix="/study-sessions", tags=["Study Sessions"])

class RecordSessionRequest(BaseModel):
    subject_id: Optional[str] = None
    topic_title: Optional[str] = None
    duration_minutes: int = Field(..., ge=1, le=1440)
    session_type: str = "pomodoro" # pomodoro | custom | review
    notes: Optional[str] = None
    productivity_rating: int = Field(4, ge=1, le=5)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class StudySessionResponse(BaseModel):
    id: str
    user_id: str
    subject_id: Optional[str] = None
    topic_title: Optional[str] = None
    session_type: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    xp_earned: int
    notes: Optional[str] = None
    productivity_rating: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("", response_model=List[StudySessionResponse])
def list_sessions(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = StudyService(db)
    return svc.list_sessions(current_user.id, limit=limit)

@router.post("", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
def record_session(
    data: RecordSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = StudyService(db)
    return svc.record_study_session(
        user_id=current_user.id,
        subject_id=data.subject_id,
        topic_title=data.topic_title,
        duration_minutes=data.duration_minutes,
        session_type=data.session_type,
        notes=data.notes,
        productivity_rating=data.productivity_rating,
        start_time=data.start_time,
        end_time=data.end_time
    )
