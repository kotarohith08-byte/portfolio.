"""
StudyChart AI - Quizzes API Endpoints.
"""

import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.quiz_service import QuizService
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    SubmitQuizAttemptRequest,
    QuizAttemptResponse,
    QuizQuestionResponse,
    QuizAnswerResult
)

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

def serialize_quiz(q) -> dict:
    questions_list = []
    for qu in q.questions:
        opts = json.loads(qu.options) if qu.options else []
        questions_list.append({
            "id": qu.id,
            "quiz_id": qu.quiz_id,
            "question_text": qu.question_text,
            "question_type": qu.question_type,
            "options": opts,
            "order_index": qu.order_index
        })
    return {
        "id": q.id,
        "user_id": q.user_id,
        "subject_id": q.subject_id,
        "title": q.title,
        "topic": q.topic,
        "difficulty": q.difficulty,
        "total_questions": q.total_questions,
        "is_ai_generated": q.is_ai_generated,
        "questions": questions_list,
        "created_at": q.created_at
    }

@router.get("", response_model=List[QuizResponse])
def list_quizzes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc = QuizService(db)
    quizzes = svc.list_quizzes(current_user.id)
    return [serialize_quiz(q) for q in quizzes]

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc = QuizService(db)
    quiz = svc.get_quiz(quiz_id, current_user.id)
    return serialize_quiz(quiz)

@router.post("/{quiz_id}/attempt", response_model=QuizAttemptResponse)
def submit_attempt(
    quiz_id: str,
    data: SubmitQuizAttemptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = QuizService(db)
    att = svc.submit_quiz_attempt(quiz_id, current_user.id, data)

    answers_res = []
    for a in att.answers:
        q_text = a.question.question_text if a.question else ""
        correct_ans = a.question.correct_answer if a.question else ""
        answers_res.append(QuizAnswerResult(
            question_id=a.question_id,
            question_text=q_text,
            user_answer=a.user_answer or "",
            correct_answer=correct_ans,
            is_correct=a.is_correct,
            explanation=a.explanation
        ))

    xp = int(att.score * 0.5) + (att.correct_count * 10)
    return QuizAttemptResponse(
        id=att.id,
        quiz_id=att.quiz_id,
        score=att.score,
        correct_count=att.correct_count,
        total_count=att.total_count,
        time_taken_seconds=att.time_taken_seconds,
        ai_feedback=att.ai_feedback,
        answers=answers_res,
        xp_earned=xp,
        created_at=att.created_at
    )
