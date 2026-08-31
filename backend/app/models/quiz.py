"""
StudyChart AI - Quiz, Question, Attempt, and Answer SQLAlchemy Models.
"""

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class Quiz(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "quizzes"

    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="intermediate", nullable=False) # easy | intermediate | hard
    total_questions = Column(Integer, default=5, nullable=False)
    is_ai_generated = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="quizzes")
    subject = relationship("Subject", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan", order_by="QuizQuestion.order_index")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "quiz_questions"

    quiz_id = Column(String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="mcq", nullable=False) # mcq | true_false | short_answer | code
    options = Column(Text, nullable=True) # JSON array of options: ["Option A", "Option B", ...]
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question", cascade="all, delete-orphan")

class QuizAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "quiz_attempts"

    quiz_id = Column(String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, default=0.0, nullable=False) # percentage 0 to 100
    correct_count = Column(Integer, default=0, nullable=False)
    total_count = Column(Integer, default=0, nullable=False)
    time_taken_seconds = Column(Integer, default=0, nullable=False)
    ai_feedback = Column(Text, nullable=True)

    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("QuizAnswer", back_populates="attempt", cascade="all, delete-orphan")

class QuizAnswer(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "quiz_answers"

    attempt_id = Column(String(36), ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    explanation = Column(Text, nullable=True)

    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("QuizQuestion", back_populates="answers")
