"""
StudyChart AI - Authentication API Endpoints.
"""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.auth_service import AuthService
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.core.rate_limiter import check_rate_limit

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(req_body: UserRegisterRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, limit_type="auth_register", max_requests=15, window_seconds=60)
    auth_svc = AuthService(db)
    return auth_svc.register(req_body)

@router.post("/login", response_model=TokenResponse)
def login_user(req_body: UserLoginRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, limit_type="auth_login", max_requests=20, window_seconds=60)
    auth_svc = AuthService(db)
    return auth_svc.login(req_body)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(req_body: RefreshTokenRequest, db: Session = Depends(get_db)):
    auth_svc = AuthService(db)
    return auth_svc.refresh(req_body.refresh_token)

@router.post("/forgot-password")
def forgot_password(req_body: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, limit_type="auth_forgot", max_requests=10, window_seconds=60)
    auth_svc = AuthService(db)
    return auth_svc.forgot_password(req_body.email)

@router.post("/reset-password")
def reset_password(req_body: ResetPasswordRequest, db: Session = Depends(get_db)):
    auth_svc = AuthService(db)
    auth_svc.reset_password(req_body.token, req_body.new_password)
    return {"success": True, "message": "Password reset successfully. You may now log in."}
