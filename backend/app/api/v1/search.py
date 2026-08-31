"""
StudyChart AI - Global Indexed Search API.
Searches across user's subjects, topics, notes, and quizzes.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.subject import Subject, Topic, Unit
from app.models.note import Note
from app.models.quiz import Quiz

router = APIRouter(prefix="/search", tags=["Global Search"])

@router.get("")
def search_all(
    q: str = Query(..., min_length=1, max_length=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    term = f"%{q.strip().lower()}%"

    # Search Subjects
    subjects = db.query(Subject).filter(
        Subject.user_id == current_user.id,
        (Subject.name.ilike(term)) | (Subject.description.ilike(term))
    ).limit(5).all()

    # Search Notes
    notes = db.query(Note).filter(
        Note.user_id == current_user.id,
        (Note.title.ilike(term)) | (Note.content.ilike(term)) | (Note.tags.ilike(term))
    ).limit(5).all()

    # Search Quizzes
    quizzes = db.query(Quiz).filter(
        Quiz.user_id == current_user.id,
        (Quiz.title.ilike(term)) | (Quiz.topic.ilike(term))
    ).limit(5).all()

    return {
        "query": q,
        "results": {
            "subjects": [{"id": s.id, "title": s.name, "type": "subject", "color": s.color, "icon": s.icon} for s in subjects],
            "notes": [{"id": n.id, "title": n.title, "type": "note", "tags": n.tags} for n in notes],
            "quizzes": [{"id": qz.id, "title": qz.title, "type": "quiz", "topic": qz.topic, "difficulty": qz.difficulty} for qz in quizzes]
        }
    }
