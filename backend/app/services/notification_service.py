"""
StudyChart AI - Notification Service.
"""

from typing import List
from sqlalchemy.orm import Session
from app.models.notification import Notification

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_notifications(self, user_id: str, limit: int = 20) -> List[Notification]:
        return self.db.query(Notification).filter(
            Notification.user_id == user_id
        ).order_by(Notification.created_at.desc()).limit(limit).all()

    def mark_as_read(self, notif_id: str, user_id: str) -> None:
        self.db.query(Notification).filter(
            Notification.id == notif_id,
            Notification.user_id == user_id
        ).update({"is_read": True})
        self.db.commit()

    def mark_all_as_read(self, user_id: str) -> None:
        self.db.query(Notification).filter(
            Notification.user_id == user_id
        ).update({"is_read": True})
        self.db.commit()
