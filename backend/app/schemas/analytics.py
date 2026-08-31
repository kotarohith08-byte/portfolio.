"""
StudyChart AI - Analytics & Dashboard Pydantic Schemas.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DailyStudyPoint(BaseModel):
    day: str  # "Mon", "Tue", or "2026-08-30"
    minutes: int

class SubjectProgressItem(BaseModel):
    subject_id: str
    subject_name: str
    color: str
    icon: str
    total_minutes: int
    completion_percentage: float
    mastery_score: float

class TopicAccuracyItem(BaseModel):
    topic: str
    accuracy: float
    total_questions: int
    status: str # "weak" | "average" | "strong"

class DashboardSummaryResponse(BaseModel):
    today_goal_minutes: int
    today_completed_minutes: int
    today_progress_percentage: float
    current_streak_days: int
    longest_streak_days: int
    total_study_hours: float
    total_sessions_count: int
    average_quiz_score: float
    weekly_study_data: List[DailyStudyPoint]
    subject_progress: List[SubjectProgressItem]
    recent_quiz_scores: List[Dict[str, Any]]
    weak_topics: List[str]
    strong_topics: List[str]
    ai_insight: str
    recommended_actions: List[str]

class AnalyticsReportResponse(BaseModel):
    total_study_minutes: int
    total_study_hours: float
    weekly_total_minutes: int
    monthly_total_minutes: int
    average_session_minutes: float
    completion_rate: float
    streak_days: int
    daily_history: List[DailyStudyPoint]
    subject_distribution: List[Dict[str, Any]]
    topic_accuracies: List[TopicAccuracyItem]
    weak_topics: List[str]
    strong_topics: List[str]
    improvement_rate: float
    predicted_next_week_hours: float
