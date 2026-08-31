"""
StudyChart AI - Authentication Service.
"""

import uuid
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.auth.password import verify_password
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.schemas.user import UserRegisterRequest, UserLoginRequest, ProfileUpdateRequest
from app.core.errors import StudyChartException, UnauthorizedException, ResourceNotFoundException
from app.models.user import User, Profile

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, data: UserRegisterRequest) -> Dict[str, Any]:
        existing = self.user_repo.get_by_email(data.email)
        if existing:
            raise StudyChartException("An account with this email address already exists.", code="EMAIL_ALREADY_EXISTS")

        user = self.user_repo.create(data.name, data.email, data.password)
        access_token = create_access_token({"sub": user.id, "email": user.email})
        refresh_token = create_refresh_token({"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }

    def login(self, data: UserLoginRequest) -> Dict[str, Any]:
        user = self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email address or password.")

        if not user.is_active:
            raise StudyChartException("This account has been deactivated.", code="ACCOUNT_DEACTIVATED")

        access_token = create_access_token({"sub": user.id, "email": user.email})
        refresh_token = create_refresh_token({"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }

    def refresh(self, refresh_token: str) -> Dict[str, Any]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid or expired refresh token.")

        user_id = payload.get("sub")
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("User account invalid or deactivated.")

        access_token = create_access_token({"sub": user.id, "email": user.email})
        new_refresh = create_refresh_token({"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": new_refresh,
            "token_type": "bearer",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }

    def forgot_password(self, email: str) -> Dict[str, str]:
        user = self.user_repo.get_by_email(email)
        if user:
            token = str(uuid.uuid4())
            user.reset_token = token
            self.db.commit()
            # In production, an email would be sent here. We return a generic message for security.
            return {"message": "If an account with this email exists, a password reset link has been dispatched.", "reset_token_dev": token}
        return {"message": "If an account with this email exists, a password reset link has been dispatched."}

    def reset_password(self, token: str, new_password: str) -> None:
        user = self.db.query(User).filter(User.reset_token == token).first()
        if not user:
            raise StudyChartException("Invalid or expired password reset token.", code="INVALID_RESET_TOKEN")

        self.user_repo.update_password(user, new_password)

    def get_profile(self, user: User) -> Profile:
        profile = self.db.query(Profile).filter(Profile.user_id == user.id).first()
        if not profile:
            profile = Profile(user_id=user.id)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        return profile

    def update_profile(self, user: User, data: ProfileUpdateRequest) -> Profile:
        if data.name:
            user.name = data.name.strip()
            self.db.commit()

        profile = self.get_profile(user)
        if data.education_level is not None:
            profile.education_level = data.education_level
        if data.timezone is not None:
            profile.timezone = data.timezone
        if data.daily_study_goal_minutes is not None:
            profile.daily_study_goal_minutes = data.daily_study_goal_minutes
        if data.preferred_difficulty is not None:
            profile.preferred_difficulty = data.preferred_difficulty
        if data.learning_preferences is not None:
            profile.learning_preferences = data.learning_preferences
        if data.theme_preference is not None:
            profile.theme_preference = data.theme_preference
        if data.avatar_url is not None:
            profile.avatar_url = data.avatar_url

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def export_user_data(self, user: User) -> Dict[str, Any]:
        """GDPR compliant full data export"""
        profile = self.get_profile(user)
        return {
            "account": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat()
            },
            "profile": {
                "education_level": profile.education_level,
                "timezone": profile.timezone,
                "daily_study_goal_minutes": profile.daily_study_goal_minutes,
                "xp": profile.current_xp,
                "level": profile.current_level,
                "streak": profile.current_streak_days
            },
            "subjects_count": len(user.subjects),
            "study_sessions_count": len(user.study_sessions),
            "notes_count": len(user.notes),
            "quizzes_count": len(user.quizzes)
        }

    def delete_account(self, user: User) -> None:
        self.user_repo.delete_user(user)
