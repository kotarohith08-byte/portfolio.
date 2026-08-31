"""
StudyChart AI - AI Orchestration Endpoints.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.study_plan import GeneratePlanRequest
from app.schemas.quiz import GenerateQuizRequest
from app.schemas.ai import AITutorMessageRequest, AITutorResponse
from app.ai.study_planner import ai_study_planner
from app.ai.quiz_generator import ai_quiz_generator
from app.ai.tutor import ai_tutor
from app.ai.performance_analyzer import ai_performance_analyzer
from app.ai.cost_control import ai_cost_controller
from app.core.rate_limiter import check_rate_limit
from app.services.quiz_service import QuizService
from app.repositories.quiz_repo import QuizRepository

router = APIRouter(prefix="/ai", tags=["AI Services"])

@router.post("/study-plan")
def generate_study_plan(
    req: GeneratePlanRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_rate_limit(request, limit_type="ai_plan", max_requests=10, window_seconds=60)
    ai_cost_controller.log_and_check_quota(db, current_user.id, endpoint="study_plan")
    return ai_study_planner.generate_plan(req)

@router.post("/quiz")
def generate_ai_quiz(
    req: GenerateQuizRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_rate_limit(request, limit_type="ai_quiz", max_requests=15, window_seconds=60)
    ai_cost_controller.log_and_check_quota(db, current_user.id, endpoint="quiz_gen")
    quiz_data = ai_quiz_generator.generate_quiz(req)

    # Persist the generated quiz directly for the user
    quiz_repo = QuizRepository(db)
    quiz_obj = quiz_repo.create_quiz_for_user(
        user_id=current_user.id,
        subject_id=req.subject_id,
        title=quiz_data.get("title", f"Quiz: {req.topic}"),
        topic=req.topic,
        difficulty=req.difficulty,
        questions_data=quiz_data.get("questions", [])
    )

    from app.api.v1.quizzes import serialize_quiz
    return serialize_quiz(quiz_obj)

@router.post("/tutor", response_model=AITutorResponse)
def chat_with_tutor(
    req: AITutorMessageRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_rate_limit(request, limit_type="ai_tutor", max_requests=30, window_seconds=60)
    ai_cost_controller.log_and_check_quota(db, current_user.id, endpoint="tutor")
    return ai_tutor.handle_message(db, current_user.id, req)

@router.post("/analyze-performance")
def analyze_student_performance(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_rate_limit(request, limit_type="ai_analysis", max_requests=10, window_seconds=60)
    ai_cost_controller.log_and_check_quota(db, current_user.id, endpoint="performance_analyzer")
    return ai_performance_analyzer.analyze(db, current_user.id)
