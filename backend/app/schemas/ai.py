"""
StudyChart AI - AI Layer Schemas (Structured Output validation).
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AITutorMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    subject_id: Optional[str] = None
    topic: Optional[str] = None
    message: str = Field(..., min_length=1)
    difficulty_level: Optional[str] = "intermediate" # beginner | intermediate | advanced

class AIMessageSchema(BaseModel):
    id: str
    role: str
    content: str
    created_at: str

class AITutorResponse(BaseModel):
    conversation_id: str
    message: str
    suggested_followups: List[str] = []
    code_snippet: Optional[str] = None

class AIStudyPlanItemSchema(BaseModel):
    day: str # e.g. "Monday"
    start_time: str # "09:00"
    end_time: str   # "09:45"
    activity_type: str # study | revision | quiz | practice | rest
    topic: str
    description: str

class AIStudyPlanOutput(BaseModel):
    title: str
    strategy_overview: str
    weekly_hours: int
    schedule: List[AIStudyPlanItemSchema]
    exam_readiness_tips: List[str]

class AIQuizQuestionSchema(BaseModel):
    question_text: str
    question_type: str = "mcq"
    options: List[str]
    correct_answer: str
    explanation: str

class AIQuizOutput(BaseModel):
    title: str
    topic: str
    difficulty: str
    questions: List[AIQuizQuestionSchema]

class AIPerformanceAnalysisOutput(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    study_behavior_insight: str
    immediate_recommendations: List[str]
    next_week_forecast: str
