"""
StudyChart AI - User Repository.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User, Profile
from app.auth.password import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def create(self, name: str, email: str, password: str) -> User:
        hashed_pwd = get_password_hash(password)
        user = User(
            name=name.strip(),
            email=email.lower().strip(),
            hashed_password=hashed_pwd
        )
        self.db.add(user)
        self.db.flush()

        # Create default user profile
        profile = Profile(
            user_id=user.id,
            education_level="Undergraduate",
            timezone="UTC",
            daily_study_goal_minutes=120,
            preferred_difficulty="intermediate",
            theme_preference="dark",
            current_xp=0,
            current_level=1,
            current_streak_days=0,
            longest_streak_days=0
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user: User, new_password: str) -> None:
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        self.db.commit()

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
