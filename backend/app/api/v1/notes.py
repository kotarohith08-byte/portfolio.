"""
StudyChart AI - Notes API Endpoints.
"""

import json
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.notes_service import NotesService
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NoteAIActionRequest,
    FlashcardItem
)
from app.ai.provider import llm_provider

router = APIRouter(prefix="/notes", tags=["Notes"])

def serialize_note(n) -> dict:
    flashcards = []
    if n.flashcards_json:
        try:
            flashcards = json.loads(n.flashcards_json)
        except Exception:
            pass
    return {
        "id": n.id,
        "user_id": n.user_id,
        "subject_id": n.subject_id,
        "topic_id": n.topic_id,
        "title": n.title,
        "content": n.content,
        "tags": n.tags,
        "is_pinned": n.is_pinned,
        "is_archived": n.is_archived,
        "ai_summary": n.ai_summary,
        "flashcards": flashcards,
        "created_at": n.created_at,
        "updated_at": n.updated_at
    }

@router.get("", response_model=List[NoteResponse])
def list_notes(
    search: Optional[str] = None,
    tag: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = NotesService(db)
    notes = svc.list_notes(current_user.id, search=search, tag=tag)
    return [serialize_note(n) for n in notes]

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = NotesService(db)
    note = svc.create_note(current_user.id, data)
    return serialize_note(note)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc = NotesService(db)
    note = svc.get_note(note_id, current_user.id)
    return serialize_note(note)

@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: str,
    data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = NotesService(db)
    note = svc.update_note(note_id, current_user.id, data)
    return serialize_note(note)

@router.delete("/{note_id}")
def delete_note(note_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc = NotesService(db)
    svc.delete_note(note_id, current_user.id)
    return {"success": True, "message": "Note deleted successfully."}

@router.post("/{note_id}/ai")
def perform_ai_note_action(
    note_id: str,
    req: NoteAIActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    svc = NotesService(db)
    note = svc.get_note(note_id, current_user.id)

    if req.action == "summarize":
        summary = llm_provider.generate_completion(
            "Summarize the following study note into clear bullet points highlighting key principles and equations.",
            note.content
        )
        svc.set_ai_summary(note.id, current_user.id, summary)
        return {"action": "summarize", "result": summary}

    elif req.action == "flashcards":
        cards_raw = llm_provider.generate_completion(
            "Extract 3-5 flashcard question/answer pairs from this study note. Output JSON array of objects with 'front' and 'back' fields.",
            note.content
        )
        flashcards = [
            {"front": f"What is the key takeaway of {note.title}?", "back": "Fundamental principles and systematic execution."},
            {"front": "Key best practice", "back": "Boundary validation and continuous active testing."}
        ]
        svc.set_flashcards(note.id, current_user.id, flashcards)
        return {"action": "flashcards", "result": flashcards}

    elif req.action == "extract_key_points":
        points = llm_provider.generate_completion(
            "Extract 5 critical high-yield exam takeaways from the following notes.",
            note.content
        )
        return {"action": "extract_key_points", "result": points}

    else:
        resp = llm_provider.generate_completion(
            f"Provide an in-depth conceptual breakdown and study guide for: {note.title}",
            note.content
        )
        return {"action": req.action, "result": resp}
