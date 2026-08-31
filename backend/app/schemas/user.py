"""
StudyChart AI - User and Profile Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    confirm_password: str = Field(..., min_length=6, max_length=128)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match.")
        return v

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6, max_length=128)

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    education_level: Optional[str] = None
    timezone: Optional[str] = None
    daily_study_goal_minutes: Optional[int] = Field(None, ge=10, le=1440)
    preferred_difficulty: Optional[str] = None
    learning_preferences: Optional[str] = None
    theme_preference: Optional[str] = None
    avatar_url: Optional[str] = None

class ProfileResponse(BaseModel):
    id: str
    user_id: str
    name: str
    email: str
    avatar_url: Optional[str] = None
    education_level: str
    timezone: str
    daily_study_goal_minutes: int
    preferred_difficulty: str
    learning_preferences: Optional[str] = None
    theme_preference: str
    current_xp: int
    current_level: int
    current_streak_days: int
    longest_streak_days: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    is_superuser: bool
    profile: Optional[ProfileResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
