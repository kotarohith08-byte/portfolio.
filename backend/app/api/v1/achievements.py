"""
StudyChart AI - Achievements API Endpoints.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.gamification_service import GamificationService

router = APIRouter(prefix="/achievements", tags=["Achievements"])

@router.get("")
def list_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    gamify_svc = GamificationService(db)
    return gamify_svc.get_user_achievements(current_user.id)
