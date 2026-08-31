"""
StudyChart AI - Notes Service.
"""

import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate
from app.models.note import Note
from app.core.errors import ResourceNotFoundException

class NotesService:
    def __init__(self, db: Session):
        self.db = db
        self.note_repo = NoteRepository(db)

    def list_notes(self, user_id: str, search: Optional[str] = None, tag: Optional[str] = None) -> List[Note]:
        return self.note_repo.get_all_for_user(user_id, search=search, tag=tag)

    def get_note(self, note_id: str, user_id: str) -> Note:
        note = self.note_repo.get_by_id_for_user(note_id, user_id)
        if not note:
            raise ResourceNotFoundException("Note not found or access denied.")
        return note

    def create_note(self, user_id: str, data: NoteCreate) -> Note:
        return self.note_repo.create_for_user(user_id, data)

    def update_note(self, note_id: str, user_id: str, data: NoteUpdate) -> Note:
        note = self.get_note(note_id, user_id)
        return self.note_repo.update_for_user(note, data)

    def delete_note(self, note_id: str, user_id: str) -> None:
        note = self.get_note(note_id, user_id)
        self.note_repo.delete_for_user(note)

    def set_ai_summary(self, note_id: str, user_id: str, summary: str) -> Note:
        note = self.get_note(note_id, user_id)
        note.ai_summary = summary
        self.db.commit()
        self.db.refresh(note)
        return note

    def set_flashcards(self, note_id: str, user_id: str, flashcards: List[Dict[str, str]]) -> Note:
        note = self.get_note(note_id, user_id)
        note.flashcards_json = json.dumps(flashcards)
        self.db.commit()
        self.db.refresh(note)
        return note
