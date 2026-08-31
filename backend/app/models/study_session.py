"""
StudyChart AI - Study Session Model.
Tracks actual active study timer logs.
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class StudySession(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "study_sessions"

    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    topic_id = Column(String(36), nullable=True)
    topic_title = Column(String(255), nullable=True)
    session_type = Column(String(50), default="pomodoro", nullable=False) # pomodoro | custom | review
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    notes = Column(Text, nullable=True)
    productivity_rating = Column(Integer, default=4, nullable=False) # 1 to 5

    user = relationship("User", back_populates="study_sessions")
    subject = relationship("Subject", back_populates="study_sessions")
