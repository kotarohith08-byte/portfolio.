"""
StudyChart AI - Notification Model.
"""

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "notifications"

    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="info", nullable=False) # info | reminder | achievement | ai | alert
    link = Column(String(512), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="notifications")
