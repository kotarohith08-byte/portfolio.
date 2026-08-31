"""
StudyChart AI - Calendar Event Model.
"""

from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class CalendarEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "calendar_events"

    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(String(50), default="study", nullable=False) # exam | deadline | study | review | quiz
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    color = Column(String(50), default="#3b82f6", nullable=False)

    user = relationship("User", back_populates="calendar_events")
