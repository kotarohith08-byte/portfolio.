"""
StudyChart AI - Database Declarative Base and Common Mixins.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class UUIDPrimaryKeyMixin:
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False, index=True)

class UserOwnedMixin:
    @declared_attr
    def user_id(cls):
        return Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
