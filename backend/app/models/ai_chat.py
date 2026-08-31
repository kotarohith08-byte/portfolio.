"""
StudyChart AI - AI Tutor Conversation, Message, and Usage Log Models.
"""

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class AIConversation(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "ai_conversations"

    title = Column(String(255), default="New Study Session", nullable=False)
    subject_id = Column(String(36), nullable=True)
    topic = Column(String(255), nullable=True)
    is_archived = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="ai_conversations")
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="AIMessage.created_at")

class AIMessage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "ai_messages"

    conversation_id = Column(String(36), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False) # user | assistant | system
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0, nullable=False)

    conversation = relationship("AIConversation", back_populates="messages")

class AIUsageLog(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "ai_usage_logs"

    endpoint = Column(String(100), nullable=False) # e.g. "tutor", "study_plan", "quiz_gen", "analyzer"
    prompt_tokens = Column(Integer, default=0, nullable=False)
    completion_tokens = Column(Integer, default=0, nullable=False)
    estimated_cost_usd = Column(Float, default=0.0, nullable=False)
    model_name = Column(String(100), nullable=False)
