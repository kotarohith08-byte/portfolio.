"""
StudyChart AI - Subject, Unit, Topic, Subtopic, Resource, Assignment Models.
"""

from sqlalchemy import Column, String, Integer, Float, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class Subject(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "subjects"

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    color = Column(String(50), default="#4f46e5", nullable=False)
    icon = Column(String(50), default="book", nullable=False)
    exam_date = Column(Date, nullable=True)
    target_grade = Column(String(10), default="A", nullable=False)
    priority = Column(Integer, default=3, nullable=False) # 1 (lowest) to 5 (highest)
    is_archived = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="subjects")
    units = relationship("Unit", back_populates="subject", cascade="all, delete-orphan", order_by="Unit.order_index")
    notes = relationship("Note", back_populates="subject", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="subject", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="subject", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="subject", cascade="all, delete-orphan")

class Unit(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "units"

    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)

    subject = relationship("Subject", back_populates="units")
    topics = relationship("Topic", back_populates="unit", cascade="all, delete-orphan", order_by="Topic.order_index")

class Topic(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "topics"

    unit_id = Column(String(36), ForeignKey("units.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    difficulty = Column(Float, default=3.0, nullable=False) # 1.0 to 5.0
    estimated_minutes = Column(Integer, default=45, nullable=False)
    mastery_score = Column(Float, default=0.0, nullable=False) # 0.0 to 100.0%
    order_index = Column(Integer, default=0, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)

    unit = relationship("Unit", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="topic", cascade="all, delete-orphan")

class Subtopic(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "subtopics"

    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)

    topic = relationship("Topic", back_populates="subtopics")

class Resource(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "resources"

    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(1024), nullable=True)
    resource_type = Column(String(50), default="link", nullable=False) # link | doc | video | book

    topic = relationship("Topic", back_populates="resources")

class Assignment(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "assignments"

    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    due_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    max_score = Column(Float, default=100.0, nullable=False)
    obtained_score = Column(Float, nullable=True)

    subject = relationship("Subject", back_populates="assignments")
