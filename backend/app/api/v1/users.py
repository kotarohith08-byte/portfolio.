"""
StudyChart AI - User Profile & Account Endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.auth_service import AuthService
from app.schemas.user import ProfileResponse, ProfileUpdateRequest, UserResponse

router = APIRouter(prefix="/me", tags=["User Profile"])

@router.get("", response_model=ProfileResponse)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_svc = AuthService(db)
    profile = auth_svc.get_profile(current_user)
    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        avatar_url=profile.avatar_url,
        education_level=profile.education_level,
        timezone=profile.timezone,
        daily_study_goal_minutes=profile.daily_study_goal_minutes,
        preferred_difficulty=profile.preferred_difficulty,
        learning_preferences=profile.learning_preferences,
        theme_preference=profile.theme_preference,
        current_xp=profile.current_xp,
        current_level=profile.current_level,
        current_streak_days=profile.current_streak_days,
        longest_streak_days=profile.longest_streak_days,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )

@router.patch("", response_model=ProfileResponse)
def update_my_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    auth_svc = AuthService(db)
    profile = auth_svc.update_profile(current_user, data)
    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        avatar_url=profile.avatar_url,
        education_level=profile.education_level,
        timezone=profile.timezone,
        daily_study_goal_minutes=profile.daily_study_goal_minutes,
        preferred_difficulty=profile.preferred_difficulty,
        learning_preferences=profile.learning_preferences,
        theme_preference=profile.theme_preference,
        current_xp=profile.current_xp,
        current_level=profile.current_level,
        current_streak_days=profile.current_streak_days,
        longest_streak_days=profile.longest_streak_days,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )

@router.get("/export")
def export_my_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_svc = AuthService(db)
    return auth_svc.export_user_data(current_user)

@router.delete("")
def delete_my_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_svc = AuthService(db)
    auth_svc.delete_account(current_user)
    return {"success": True, "message": "Your account and all associated data have been permanently deleted."}
