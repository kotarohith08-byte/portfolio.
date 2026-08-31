"""
StudyChart AI - Quiz Repository with Strict User Isolation.
"""

import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt, QuizAnswer

class QuizRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: str) -> List[Quiz]:
        return self.db.query(Quiz).options(
            joinedload(Quiz.questions)
        ).filter(Quiz.user_id == user_id).order_by(Quiz.created_at.desc()).all()

    def get_by_id_for_user(self, quiz_id: str, user_id: str) -> Optional[Quiz]:
        return self.db.query(Quiz).options(
            joinedload(Quiz.questions)
        ).filter(Quiz.id == quiz_id, Quiz.user_id == user_id).first()

    def create_quiz_for_user(
        self,
        user_id: str,
        subject_id: Optional[str],
        title: str,
        topic: str,
        difficulty: str,
        questions_data: List[Dict[str, Any]]
    ) -> Quiz:
        quiz = Quiz(
            user_id=user_id,
            subject_id=subject_id,
            title=title,
            topic=topic,
            difficulty=difficulty,
            total_questions=len(questions_data),
            is_ai_generated=True
        )
        self.db.add(quiz)
        self.db.flush()

        for idx, q_data in enumerate(questions_data):
            options_json = json.dumps(q_data.get("options", [])) if q_data.get("options") else None
            question = QuizQuestion(
                quiz_id=quiz.id,
                question_text=q_data.get("question_text", ""),
                question_type=q_data.get("question_type", "mcq"),
                options=options_json,
                correct_answer=q_data.get("correct_answer", ""),
                explanation=q_data.get("explanation", ""),
                order_index=idx
            )
            self.db.add(question)

        self.db.commit()
        self.db.refresh(quiz)
        return quiz

    def submit_attempt(
        self,
        quiz_id: str,
        user_id: str,
        time_taken_seconds: int,
        user_answers: List[Dict[str, str]],
        ai_feedback: Optional[str] = None
    ) -> QuizAttempt:
        quiz = self.get_by_id_for_user(quiz_id, user_id)
        if not quiz:
            raise ValueError("Quiz not found or unauthorized.")

        questions_by_id = {q.id: q for q in quiz.questions}
        correct_count = 0
        total_count = len(quiz.questions)

        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=user_id,
            total_count=total_count,
            time_taken_seconds=time_taken_seconds,
            ai_feedback=ai_feedback
        )
        self.db.add(attempt)
        self.db.flush()

        user_ans_map = {item["question_id"]: item["user_answer"] for item in user_answers}

        for q_id, q in questions_by_id.items():
            u_ans = user_ans_map.get(q_id, "").strip()
            is_correct = (u_ans.lower() == q.correct_answer.strip().lower())
            if is_correct:
                correct_count += 1

            ans_obj = QuizAnswer(
                attempt_id=attempt.id,
                question_id=q_id,
                user_answer=u_ans,
                is_correct=is_correct,
                explanation=q.explanation
            )
            self.db.add(ans_obj)

        score_pct = (correct_count / total_count * 100.0) if total_count > 0 else 0.0
        attempt.score = round(score_pct, 2)
        attempt.correct_count = correct_count

        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def get_recent_attempts_for_user(self, user_id: str, limit: int = 10) -> List[QuizAttempt]:
        return self.db.query(QuizAttempt).options(
            joinedload(QuizAttempt.answers),
            joinedload(QuizAttempt.quiz)
        ).filter(QuizAttempt.user_id == user_id).order_by(QuizAttempt.created_at.desc()).limit(limit).all()
