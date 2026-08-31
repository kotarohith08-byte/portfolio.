"""
StudyChart AI - Note SQLAlchemy Model.
"""

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class Note(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "notes"

    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    topic_id = Column(String(36), nullable=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    tags = Column(String(512), nullable=True) # comma-separated tags e.g. "sql,joins,dbms"
    is_pinned = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    ai_summary = Column(Text, nullable=True)
    flashcards_json = Column(Text, nullable=True) # JSON array of {front: ..., back: ...}

    user = relationship("User", back_populates="notes")
    subject = relationship("Subject", back_populates="notes")
