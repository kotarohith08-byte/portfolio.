"""
StudyChart AI - Quiz, Question, Attempt Schemas.
"""

from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field

class QuizQuestionCreate(BaseModel):
    question_text: str
    question_type: str = "mcq" # mcq | true_false | short_answer | code
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    order_index: int = 0

class QuizQuestionResponse(BaseModel):
    id: str
    quiz_id: str
    question_text: str
    question_type: str
    options: Optional[List[str]] = None
    order_index: int

    class Config:
        from_attributes = True

class QuizCreate(BaseModel):
    subject_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    topic: str
    difficulty: str = "intermediate"
    total_questions: int = Field(5, ge=1, le=50)
    questions: Optional[List[QuizQuestionCreate]] = None

class QuizResponse(BaseModel):
    id: str
    user_id: str
    subject_id: Optional[str] = None
    title: str
    topic: str
    difficulty: str
    total_questions: int
    is_ai_generated: bool
    questions: List[QuizQuestionResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class GenerateQuizRequest(BaseModel):
    subject_id: Optional[str] = None
    topic: str
    difficulty: str = "intermediate" # easy | intermediate | hard
    number_of_questions: int = Field(5, ge=1, le=20)
    question_type: str = "mcq" # mcq | true_false | mixed | code

class SubmitAnswerItem(BaseModel):
    question_id: str
    user_answer: str

class SubmitQuizAttemptRequest(BaseModel):
    time_taken_seconds: int = 0
    answers: List[SubmitAnswerItem]

class QuizAnswerResult(BaseModel):
    question_id: str
    question_text: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    explanation: Optional[str] = None

class QuizAttemptResponse(BaseModel):
    id: str
    quiz_id: str
    score: float
    correct_count: int
    total_count: int
    time_taken_seconds: int
    ai_feedback: Optional[str] = None
    answers: List[QuizAnswerResult] = []
    xp_earned: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
