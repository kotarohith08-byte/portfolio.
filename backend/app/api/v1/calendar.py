"""
StudyChart AI - Calendar API Endpoints.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.calendar import CalendarEvent
from app.core.errors import ResourceNotFoundException

router = APIRouter(prefix="/calendar", tags=["Calendar"])

class CalendarEventCreate(BaseModel):
    subject_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    event_type: str = "study" # exam | deadline | study | review | quiz
    start_time: datetime
    end_time: datetime
    color: str = "#3b82f6"

class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_completed: Optional[bool] = None
    color: Optional[str] = None

class CalendarEventResponse(BaseModel):
    id: str
    user_id: str
    subject_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    event_type: str
    start_time: datetime
    end_time: datetime
    is_completed: bool
    color: str

    class Config:
        from_attributes = True

@router.get("", response_model=List[CalendarEventResponse])
def list_calendar_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(CalendarEvent).filter(CalendarEvent.user_id == current_user.id)
    if start_date:
        query = query.filter(CalendarEvent.start_time >= start_date)
    if end_date:
        query = query.filter(CalendarEvent.end_time <= end_date)
    return query.order_by(CalendarEvent.start_time.asc()).all()

@router.post("", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
def create_calendar_event(
    data: CalendarEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = CalendarEvent(
        user_id=current_user.id,
        subject_id=data.subject_id,
        title=data.title.strip(),
        description=data.description,
        event_type=data.event_type,
        start_time=data.start_time,
        end_time=data.end_time,
        color=data.color
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.patch("/{event_id}", response_model=CalendarEventResponse)
def update_calendar_event(
    event_id: str,
    data: CalendarEventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    if not event:
        raise ResourceNotFoundException("Calendar event not found or access denied.")

    if data.title is not None:
        event.title = data.title.strip()
    if data.description is not None:
        event.description = data.description
    if data.event_type is not None:
        event.event_type = data.event_type
    if data.start_time is not None:
        event.start_time = data.start_time
    if data.end_time is not None:
        event.end_time = data.end_time
    if data.is_completed is not None:
        event.is_completed = data.is_completed
    if data.color is not None:
        event.color = data.color

    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_calendar_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    if not event:
        raise ResourceNotFoundException("Calendar event not found or access denied.")

    db.delete(event)
    db.commit()
    return {"success": True, "message": "Calendar event deleted."}
