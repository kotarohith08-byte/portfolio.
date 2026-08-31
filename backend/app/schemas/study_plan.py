"""
StudyChart AI - Study Plan Pydantic Schemas.
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class StudyPlanItemCreate(BaseModel):
    subject_id: Optional[str] = None
    topic_title: str
    activity_type: str = "study" # study | revision | quiz | practice | rest
    scheduled_date: date
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_minutes: int = 45
    notes: Optional[str] = None

class StudyPlanItemUpdate(BaseModel):
    is_completed: Optional[bool] = None
    topic_title: Optional[str] = None
    activity_type: Optional[str] = None
    scheduled_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None

class StudyPlanItemResponse(BaseModel):
    id: str
    study_plan_id: str
    subject_id: Optional[str] = None
    topic_title: str
    activity_type: str
    scheduled_date: date
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_minutes: int
    is_completed: bool
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class StudyPlanCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_exam_date: Optional[date] = None
    daily_available_hours: int = Field(3, ge=1, le=16)
    strategy_summary: Optional[str] = None
    items: Optional[List[StudyPlanItemCreate]] = None

class StudyPlanResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    target_exam_date: Optional[date] = None
    daily_available_hours: int
    strategy_summary: Optional[str] = None
    is_active: bool
    items: List[StudyPlanItemResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GeneratePlanRequest(BaseModel):
    subject_names: List[str]
    exam_date: Optional[date] = None
    daily_hours: int = Field(3, ge=1, le=16)
    difficult_topics: Optional[List[str]] = None
    important_topics: Optional[List[str]] = None
    preferred_study_time: Optional[str] = "morning" # morning | afternoon | evening | night
    learning_style: Optional[str] = "balanced" # intensive | balanced | relaxed
