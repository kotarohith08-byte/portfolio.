"""
StudyChart AI - Subjects API Endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.subject_service import SubjectService
from app.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    UnitCreate,
    UnitResponse,
    TopicCreate,
    TopicResponse
)

router = APIRouter(prefix="/subjects", tags=["Subjects"])

def serialize_subject(s) -> dict:
    total_topics = 0
    completed_topics = 0
    units_data = []

    for u in s.units:
        topics_data = []
        for t in u.topics:
            total_topics += 1
            if t.is_completed:
                completed_topics += 1
            topics_data.append({
                "id": t.id,
                "unit_id": t.unit_id,
                "title": t.title,
                "description": t.description,
                "difficulty": t.difficulty,
                "estimated_minutes": t.estimated_minutes,
                "mastery_score": t.mastery_score,
                "order_index": t.order_index,
                "is_completed": t.is_completed,
                "subtopics": [{"id": st.id, "topic_id": st.topic_id, "title": st.title, "is_completed": st.is_completed} for st in t.subtopics],
                "resources": [{"id": r.id, "topic_id": r.topic_id, "title": r.title, "url": r.url, "resource_type": r.resource_type} for r in t.resources]
            })
        units_data.append({
            "id": u.id,
            "subject_id": u.subject_id,
            "title": u.title,
            "description": u.description,
            "order_index": u.order_index,
            "topics": topics_data
        })

    pct = (completed_topics / total_topics * 100.0) if total_topics > 0 else 0.0
    return {
        "id": s.id,
        "user_id": s.user_id,
        "name": s.name,
        "description": s.description,
        "color": s.color,
        "icon": s.icon,
        "exam_date": s.exam_date,
        "target_grade": s.target_grade,
        "priority": s.priority,
        "is_archived": s.is_archived,
        "units": units_data,
        "total_topics": total_topics,
        "completed_topics": completed_topics,
        "progress_percentage": round(pct, 1),
        "created_at": s.created_at,
        "updated_at": s.updated_at
    }

@router.get("", response_model=List[SubjectResponse])
def list_subjects(
    include_archived: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = SubjectService(db)
    subjects = svc.list_subjects(current_user.id, include_archived=include_archived)
    return [serialize_subject(s) for s in subjects]

@router.post("", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    data: SubjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = SubjectService(db)
    subj = svc.create_subject(current_user.id, data)
    return serialize_subject(subj)

@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = SubjectService(db)
    subj = svc.get_subject(subject_id, current_user.id)
    return serialize_subject(subj)

@router.patch("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: str,
    data: SubjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = SubjectService(db)
    subj = svc.update_subject(subject_id, current_user.id, data)
    return serialize_subject(subj)

@router.delete("/{subject_id}")
def delete_subject(
    subject_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = SubjectService(db)
    svc.delete_subject(subject_id, current_user.id)
    return {"success": True, "message": "Subject deleted successfully."}

@router.post("/{subject_id}/units", response_model=UnitResponse, status_code=status.HTTP_201_CREATED)
def add_unit_to_subject(
    subject_id: str,
    data: UnitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = SubjectService(db)
    unit = svc.add_unit(subject_id, current_user.id, data)
    return unit
