"""
StudyChart AI - Study Service (Plans and Timer Sessions).
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.repositories.study_repo import StudyRepository
from app.schemas.study_plan import StudyPlanCreate, StudyPlanItemUpdate
from app.models.study_plan import StudyPlan, StudyPlanItem
from app.models.study_session import StudySession
from app.core.errors import ResourceNotFoundException
from app.services.gamification_service import GamificationService

class StudyService:
    def __init__(self, db: Session):
        self.db = db
        self.study_repo = StudyRepository(db)
        self.gamify_svc = GamificationService(db)

    def get_user_plans(self, user_id: str) -> List[StudyPlan]:
        return self.study_repo.get_plans_for_user(user_id)

    def get_active_plan(self, user_id: str) -> Optional[StudyPlan]:
        return self.study_repo.get_active_plan_for_user(user_id)

    def create_plan(self, user_id: str, data: StudyPlanCreate) -> StudyPlan:
        return self.study_repo.create_plan_for_user(user_id, data)

    def update_plan_item(self, item_id: str, user_id: str, data: StudyPlanItemUpdate) -> StudyPlanItem:
        item = self.study_repo.update_plan_item(item_id, user_id, data)
        if not item:
            raise ResourceNotFoundException("Study plan item not found or access denied.")
        if data.is_completed:
            self.gamify_svc.award_xp(user_id, 25, "Completed study task")
        return item

    def record_study_session(
        self,
        user_id: str,
        subject_id: Optional[str],
        topic_title: Optional[str],
        duration_minutes: int,
        session_type: str = "pomodoro",
        notes: Optional[str] = None,
        productivity_rating: int = 4,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> StudySession:
        session = self.study_repo.create_session_for_user(
            user_id=user_id,
            subject_id=subject_id,
            topic_title=topic_title,
            duration_minutes=duration_minutes,
            session_type=session_type,
            notes=notes,
            productivity_rating=productivity_rating,
            start_time=start_time,
            end_time=end_time
        )
        self.gamify_svc.award_xp(user_id, session.xp_earned, f"Study Session ({duration_minutes}m)")
        self.gamify_svc.check_study_achievements(user_id)
        return session

    def list_sessions(self, user_id: str, limit: int = 50) -> List[StudySession]:
        return self.study_repo.get_sessions_for_user(user_id, limit=limit)
