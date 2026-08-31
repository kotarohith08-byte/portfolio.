"""
StudyChart AI - Analytics API Endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsReportResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("", response_model=AnalyticsReportResponse)
def get_analytics_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = AnalyticsService(db)
    return svc.get_comprehensive_analytics(current_user.id)
