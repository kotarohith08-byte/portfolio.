"""
StudyChart AI - Notes Repository with Strict User Isolation.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: str, search: Optional[str] = None, tag: Optional[str] = None) -> List[Note]:
        query = self.db.query(Note).filter(Note.user_id == user_id, Note.is_archived == False)

        if search:
            term = f"%{search.strip().lower()}%"
            query = query.filter(
                (Note.title.ilike(term)) | (Note.content.ilike(term)) | (Note.tags.ilike(term))
            )

        if tag:
            query = query.filter(Note.tags.ilike(f"%{tag.strip()}%"))

        return query.order_by(Note.is_pinned.desc(), Note.updated_at.desc()).all()

    def get_by_id_for_user(self, note_id: str, user_id: str) -> Optional[Note]:
        return self.db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()

    def create_for_user(self, user_id: str, data: NoteCreate) -> Note:
        note = Note(
            user_id=user_id,
            subject_id=data.subject_id,
            topic_id=data.topic_id,
            title=data.title.strip(),
            content=data.content,
            tags=data.tags,
            is_pinned=data.is_pinned
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update_for_user(self, note: Note, data: NoteUpdate) -> Note:
        if data.title is not None:
            note.title = data.title.strip()
        if data.content is not None:
            note.content = data.content
        if data.subject_id is not None:
            note.subject_id = data.subject_id
        if data.topic_id is not None:
            note.topic_id = data.topic_id
        if data.tags is not None:
            note.tags = data.tags
        if data.is_pinned is not None:
            note.is_pinned = data.is_pinned
        if data.is_archived is not None:
            note.is_archived = data.is_archived

        self.db.commit()
        self.db.refresh(note)
        return note

    def delete_for_user(self, note: Note) -> None:
        self.db.delete(note)
        self.db.commit()
