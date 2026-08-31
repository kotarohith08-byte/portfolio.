"""
StudyChart AI - Study Plan and Study Plan Items Models.
"""

from sqlalchemy import Column, String, Integer, Text, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class StudyPlan(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "study_plans"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_exam_date = Column(Date, nullable=True)
    daily_available_hours = Column(Integer, default=3, nullable=False)
    strategy_summary = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="study_plans")
    items = relationship("StudyPlanItem", back_populates="study_plan", cascade="all, delete-orphan", order_by="StudyPlanItem.scheduled_date, StudyPlanItem.start_time")

class StudyPlanItem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "study_plan_items"

    study_plan_id = Column(String(36), ForeignKey("study_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(String(36), nullable=True)
    topic_title = Column(String(255), nullable=False)
    activity_type = Column(String(50), default="study", nullable=False) # study | revision | quiz | practice | rest
    scheduled_date = Column(Date, nullable=False, index=True)
    start_time = Column(String(10), nullable=True) # e.g. "09:00"
    end_time = Column(String(10), nullable=True)   # e.g. "09:45"
    duration_minutes = Column(Integer, default=45, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)

    study_plan = relationship("StudyPlan", back_populates="items")
