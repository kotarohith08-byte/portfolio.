"""
StudyChart AI - Quiz Service.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.quiz_repo import QuizRepository
from app.schemas.quiz import QuizCreate, SubmitQuizAttemptRequest
from app.models.quiz import Quiz, QuizAttempt
from app.core.errors import ResourceNotFoundException
from app.services.gamification_service import GamificationService

class QuizService:
    def __init__(self, db: Session):
        self.db = db
        self.quiz_repo = QuizRepository(db)
        self.gamify_svc = GamificationService(db)

    def list_quizzes(self, user_id: str) -> List[Quiz]:
        return self.quiz_repo.get_all_for_user(user_id)

    def get_quiz(self, quiz_id: str, user_id: str) -> Quiz:
        quiz = self.quiz_repo.get_by_id_for_user(quiz_id, user_id)
        if not quiz:
            raise ResourceNotFoundException("Quiz not found or access denied.")
        return quiz

    def submit_quiz_attempt(self, quiz_id: str, user_id: str, data: SubmitQuizAttemptRequest) -> QuizAttempt:
        answers_payload = [{"question_id": a.question_id, "user_answer": a.user_answer} for a in data.answers]
        attempt = self.quiz_repo.submit_attempt(
            quiz_id=quiz_id,
            user_id=user_id,
            time_taken_seconds=data.time_taken_seconds,
            user_answers=answers_payload,
            ai_feedback="Great effort! Review the detailed question explanations to master missed topics."
        )

        xp_earned = int(attempt.score * 0.5) + (attempt.correct_count * 10)
        self.gamify_svc.award_xp(user_id, xp_earned, f"Quiz Completed ({attempt.score}%)")
        self.gamify_svc.check_quiz_achievements(user_id, attempt.score)

        return attempt

    def get_recent_attempts(self, user_id: str, limit: int = 10) -> List[QuizAttempt]:
        return self.quiz_repo.get_recent_attempts_for_user(user_id, limit=limit)
