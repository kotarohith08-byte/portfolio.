"""
StudyChart AI - Study Repository with Strict User Isolation.
"""

from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session, joinedload
from app.models.study_plan import StudyPlan, StudyPlanItem
from app.models.study_session import StudySession
from app.schemas.study_plan import StudyPlanCreate, StudyPlanItemCreate, StudyPlanItemUpdate

class StudyRepository:
    def __init__(self, db: Session):
        self.db = db

    # Study Plans
    def get_plans_for_user(self, user_id: str) -> List[StudyPlan]:
        return self.db.query(StudyPlan).options(
            joinedload(StudyPlan.items)
        ).filter(StudyPlan.user_id == user_id).order_by(StudyPlan.created_at.desc()).all()

    def get_active_plan_for_user(self, user_id: str) -> Optional[StudyPlan]:
        return self.db.query(StudyPlan).options(
            joinedload(StudyPlan.items)
        ).filter(StudyPlan.user_id == user_id, StudyPlan.is_active == True).order_by(StudyPlan.created_at.desc()).first()

    def get_plan_by_id_for_user(self, plan_id: str, user_id: str) -> Optional[StudyPlan]:
        return self.db.query(StudyPlan).options(
            joinedload(StudyPlan.items)
        ).filter(StudyPlan.id == plan_id, StudyPlan.user_id == user_id).first()

    def create_plan_for_user(self, user_id: str, data: StudyPlanCreate) -> StudyPlan:
        # Deactivate older plans
        self.db.query(StudyPlan).filter(StudyPlan.user_id == user_id).update({"is_active": False})

        plan = StudyPlan(
            user_id=user_id,
            title=data.title.strip(),
            description=data.description,
            target_exam_date=data.target_exam_date,
            daily_available_hours=data.daily_available_hours,
            strategy_summary=data.strategy_summary,
            is_active=True
        )
        self.db.add(plan)
        self.db.flush()

        if data.items:
            for item_in in data.items:
                item = StudyPlanItem(
                    study_plan_id=plan.id,
                    subject_id=item_in.subject_id,
                    topic_title=item_in.topic_title,
                    activity_type=item_in.activity_type,
                    scheduled_date=item_in.scheduled_date,
                    start_time=item_in.start_time,
                    end_time=item_in.end_time,
                    duration_minutes=item_in.duration_minutes,
                    notes=item_in.notes
                )
                self.db.add(item)

        self.db.commit()
        self.db.refresh(plan)
        return plan

    def update_plan_item(self, item_id: str, user_id: str, data: StudyPlanItemUpdate) -> Optional[StudyPlanItem]:
        item = self.db.query(StudyPlanItem).join(StudyPlan).filter(
            StudyPlanItem.id == item_id,
            StudyPlan.user_id == user_id
        ).first()

        if not item:
            return None

        if data.is_completed is not None:
            item.is_completed = data.is_completed
        if data.topic_title is not None:
            item.topic_title = data.topic_title
        if data.activity_type is not None:
            item.activity_type = data.activity_type
        if data.scheduled_date is not None:
            item.scheduled_date = data.scheduled_date
        if data.start_time is not None:
            item.start_time = data.start_time
        if data.end_time is not None:
            item.end_time = data.end_time
        if data.duration_minutes is not None:
            item.duration_minutes = data.duration_minutes
        if data.notes is not None:
            item.notes = data.notes

        self.db.commit()
        self.db.refresh(item)
        return item

    # Study Sessions
    def create_session_for_user(
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
        now = datetime.utcnow()
        st = start_time or now
        et = end_time or now
        xp = int(duration_minutes * 1.5) # 1.5 XP per study minute

        session = StudySession(
            user_id=user_id,
            subject_id=subject_id,
            topic_title=topic_title,
            session_type=session_type,
            start_time=st,
            end_time=et,
            duration_minutes=duration_minutes,
            xp_earned=xp,
            notes=notes,
            productivity_rating=productivity_rating
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_sessions_for_user(self, user_id: str, limit: int = 50) -> List[StudySession]:
        return self.db.query(StudySession).filter(
            StudySession.user_id == user_id
        ).order_by(StudySession.start_time.desc()).limit(limit).all()
