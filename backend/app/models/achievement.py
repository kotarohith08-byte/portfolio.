"""
StudyChart AI - Gamification and Achievement Models.
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class Achievement(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "achievements"

    code = Column(String(100), unique=True, index=True, nullable=False) # e.g. "streak_7", "quiz_100", "first_subject"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), default="trophy", nullable=False)
    category = Column(String(50), default="study", nullable=False) # streak | quiz | study_time | coding
    xp_reward = Column(Integer, default=50, nullable=False)
    requirement_type = Column(String(50), nullable=False)
    requirement_target = Column(Integer, nullable=False)

    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")

class UserAchievement(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "user_achievements"

    achievement_id = Column(String(36), ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False, index=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_seen = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="user_achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
