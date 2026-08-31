"""
StudyChart AI - Subject, Unit, Topic, Subtopic, Resource Schemas.
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class SubtopicCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    is_completed: bool = False

class SubtopicResponse(BaseModel):
    id: str
    topic_id: str
    title: str
    is_completed: bool

    class Config:
        from_attributes = True

class ResourceCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    url: Optional[str] = None
    resource_type: str = "link"

class ResourceResponse(BaseModel):
    id: str
    topic_id: str
    title: str
    url: Optional[str] = None
    resource_type: str

    class Config:
        from_attributes = True

class TopicCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    difficulty: float = Field(3.0, ge=1.0, le=5.0)
    estimated_minutes: int = Field(45, ge=5, le=600)
    order_index: int = 0
    subtopics: Optional[List[SubtopicCreate]] = None

class TopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[float] = None
    estimated_minutes: Optional[int] = None
    mastery_score: Optional[float] = None
    is_completed: Optional[bool] = None
    order_index: Optional[int] = None

class TopicResponse(BaseModel):
    id: str
    unit_id: str
    title: str
    description: Optional[str] = None
    difficulty: float
    estimated_minutes: int
    mastery_score: float
    order_index: int
    is_completed: bool
    subtopics: List[SubtopicResponse] = []
    resources: List[ResourceResponse] = []

    class Config:
        from_attributes = True

class UnitCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    order_index: int = 0
    topics: Optional[List[TopicCreate]] = None

class UnitResponse(BaseModel):
    id: str
    subject_id: str
    title: str
    description: Optional[str] = None
    order_index: int
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True

class SubjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = "#4f46e5"
    icon: str = "book"
    exam_date: Optional[date] = None
    target_grade: str = "A"
    priority: int = Field(3, ge=1, le=5)

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    exam_date: Optional[date] = None
    target_grade: Optional[str] = None
    priority: Optional[int] = None
    is_archived: Optional[bool] = None

class SubjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    color: str
    icon: str
    exam_date: Optional[date] = None
    target_grade: str
    priority: int
    is_archived: bool
    units: List[UnitResponse] = []
    total_topics: int = 0
    completed_topics: int = 0
    progress_percentage: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
