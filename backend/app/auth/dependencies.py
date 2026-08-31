"""
StudyChart AI - Authentication Dependencies.
Enforces that every authenticated request resolves to a valid, active user.
"""

from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.auth.jwt import decode_token
from app.core.errors import UnauthorizedException, ForbiddenException

security_bearer = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> User:
    if not credentials:
        raise UnauthorizedException("Missing Authorization Bearer token.")

    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException("Invalid, expired, or malformed authentication token.")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token payload missing user identifier.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UnauthorizedException("User associated with this token no longer exists.")

    if not user.is_active:
        raise ForbiddenException("This user account has been disabled.")

    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        raise ForbiddenException("Administrator privileges required.")
    return current_user
