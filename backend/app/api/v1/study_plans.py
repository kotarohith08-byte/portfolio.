"""
StudyChart AI - Study Plans API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.study_service import StudyService
from app.schemas.study_plan import (
    StudyPlanCreate,
    StudyPlanResponse,
    StudyPlanItemUpdate,
    StudyPlanItemResponse
)
from app.core.errors import ResourceNotFoundException

router = APIRouter(prefix="/study-plans", tags=["Study Plans"])

@router.get("", response_model=List[StudyPlanResponse])
def list_plans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc = StudyService(db)
    return svc.get_user_plans(current_user.id)

@router.get("/active", response_model=Optional[StudyPlanResponse])
def get_active_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc = StudyService(db)
    plan = svc.get_active_plan(current_user.id)
    return plan

@router.post("", response_model=StudyPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    data: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = StudyService(db)
    return svc.create_plan(current_user.id, data)

@router.patch("/items/{item_id}", response_model=StudyPlanItemResponse)
def update_plan_item(
    item_id: str,
    data: StudyPlanItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = StudyService(db)
    return svc.update_plan_item(item_id, current_user.id, data)
