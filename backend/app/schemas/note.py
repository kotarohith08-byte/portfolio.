"""
StudyChart AI - Note Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class FlashcardItem(BaseModel):
    front: str
    back: str

class NoteCreate(BaseModel):
    subject_id: Optional[str] = None
    topic_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    content: str
    tags: Optional[str] = None
    is_pinned: bool = False

class NoteUpdate(BaseModel):
    subject_id: Optional[str] = None
    topic_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None

class NoteResponse(BaseModel):
    id: str
    user_id: str
    subject_id: Optional[str] = None
    topic_id: Optional[str] = None
    title: str
    content: str
    tags: Optional[str] = None
    is_pinned: bool
    is_archived: bool
    ai_summary: Optional[str] = None
    flashcards: List[FlashcardItem] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NoteAIActionRequest(BaseModel):
    action: str = Field(..., description="summarize | explain | flashcards | extract_key_points | quiz")
