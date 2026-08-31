"""
StudyChart AI - Models Package.
"""

from app.models.user import User, Profile
from app.models.subject import Subject, Unit, Topic, Subtopic, Resource, Assignment
from app.models.study_plan import StudyPlan, StudyPlanItem
from app.models.study_session import StudySession
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt, QuizAnswer
from app.models.note import Note
from app.models.calendar import CalendarEvent
from app.models.achievement import Achievement, UserAchievement
from app.models.ai_chat import AIConversation, AIMessage, AIUsageLog
from app.models.programming import ProgrammingProblem, CodeSubmission
from app.models.notification import Notification

__all__ = [
    "User",
    "Profile",
    "Subject",
    "Unit",
    "Topic",
    "Subtopic",
    "Resource",
    "Assignment",
    "StudyPlan",
    "StudyPlanItem",
    "StudySession",
    "Quiz",
    "QuizQuestion",
    "QuizAttempt",
    "QuizAnswer",
    "Note",
    "CalendarEvent",
    "Achievement",
    "UserAchievement",
    "AIConversation",
    "AIMessage",
    "AIUsageLog",
    "ProgrammingProblem",
    "CodeSubmission",
    "Notification",
]
