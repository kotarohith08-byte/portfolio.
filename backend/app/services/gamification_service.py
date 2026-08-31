"""
StudyChart AI - Gamification Service.
Handles XP, levels, streaks, and achievements.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import Profile, User
from app.models.achievement import Achievement, UserAchievement
from app.models.study_session import StudySession
from app.models.quiz import QuizAttempt
from app.models.notification import Notification

class GamificationService:
    def __init__(self, db: Session):
        self.db = db

    def award_xp(self, user_id: str, xp: int, reason: str = "") -> None:
        if xp <= 0:
            return

        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            return

        profile.current_xp += xp
        # Level formula: level = 1 + int(sqrt(total_xp / 100))
        new_level = 1 + int((profile.current_xp / 100.0) ** 0.5)
        if new_level > profile.current_level:
            profile.current_level = new_level
            # Create Level Up Notification
            notif = Notification(
                user_id=user_id,
                title="Level Up!",
                message=f"Congratulations! You've reached Level {new_level} in StudyChart AI! Keep up the momentum!",
                notification_type="achievement"
            )
            self.db.add(notif)

        self.db.commit()

    def check_study_achievements(self, user_id: str) -> None:
        # Total Study Hours
        total_mins = self.db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0)).filter(
            StudySession.user_id == user_id
        ).scalar() or 0
        total_hours = total_mins / 60.0

        if total_hours >= 10:
            self._unlock_achievement(user_id, "hours_10")
        if total_hours >= 50:
            self._unlock_achievement(user_id, "hours_50")

        # Total Sessions
        sessions_cnt = self.db.query(func.count(StudySession.id)).filter(
            StudySession.user_id == user_id
        ).scalar() or 0

        if sessions_cnt >= 1:
            self._unlock_achievement(user_id, "first_session")
        if sessions_cnt >= 50:
            self._unlock_achievement(user_id, "sessions_50")

    def check_quiz_achievements(self, user_id: str, score: float) -> None:
        attempts_count = self.db.query(func.count(QuizAttempt.id)).filter(
            QuizAttempt.user_id == user_id
        ).scalar() or 0

        if attempts_count >= 1:
            self._unlock_achievement(user_id, "first_quiz")
        if attempts_count >= 10:
            self._unlock_achievement(user_id, "quiz_10")
        if score >= 90.0:
            self._unlock_achievement(user_id, "quiz_master_90")

    def _unlock_achievement(self, user_id: str, code: str) -> None:
        ach = self.db.query(Achievement).filter(Achievement.code == code).first()
        if not ach:
            return

        exists = self.db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == ach.id
        ).first()

        if not exists:
            user_ach = UserAchievement(
                user_id=user_id,
                achievement_id=ach.id,
                unlocked_at=datetime.utcnow()
            )
            self.db.add(user_ach)

            # Award achievement XP
            profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
            if profile:
                profile.current_xp += ach.xp_reward

            # Notification
            notif = Notification(
                user_id=user_id,
                title=f"Achievement Unlocked: {ach.title}",
                message=f"{ach.description} (+{ach.xp_reward} XP)",
                notification_type="achievement"
            )
            self.db.add(notif)
            self.db.commit()

    def get_user_achievements(self, user_id: str) -> List[dict]:
        all_achs = self.db.query(Achievement).all()
        user_unlocked = {
            ua.achievement_id: ua.unlocked_at
            for ua in self.db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()
        }

        results = []
        for ach in all_achs:
            unlocked = ach.id in user_unlocked
            results.append({
                "id": ach.id,
                "code": ach.code,
                "title": ach.title,
                "description": ach.description,
                "icon": ach.icon,
                "category": ach.category,
                "xp_reward": ach.xp_reward,
                "is_unlocked": unlocked,
                "unlocked_at": user_unlocked[ach.id].isoformat() if unlocked else None
            })
        return results
