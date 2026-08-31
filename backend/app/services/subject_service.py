"""
StudyChart AI - Subject Service.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.subject_repo import SubjectRepository
from app.schemas.subject import SubjectCreate, SubjectUpdate, UnitCreate, TopicCreate
from app.models.subject import Subject, Unit, Topic
from app.core.errors import ResourceNotFoundException

class SubjectService:
    def __init__(self, db: Session):
        self.db = db
        self.subject_repo = SubjectRepository(db)

    def list_subjects(self, user_id: str, include_archived: bool = False) -> List[Subject]:
        return self.subject_repo.get_all_for_user(user_id, include_archived=include_archived)

    def get_subject(self, subject_id: str, user_id: str) -> Subject:
        subj = self.subject_repo.get_by_id_for_user(subject_id, user_id)
        if not subj:
            raise ResourceNotFoundException("Subject not found or access denied.")
        return subj

    def create_subject(self, user_id: str, data: SubjectCreate) -> Subject:
        return self.subject_repo.create_for_user(user_id, data)

    def update_subject(self, subject_id: str, user_id: str, data: SubjectUpdate) -> Subject:
        subj = self.get_subject(subject_id, user_id)
        return self.subject_repo.update_for_user(subj, data)

    def delete_subject(self, subject_id: str, user_id: str) -> None:
        subj = self.get_subject(subject_id, user_id)
        self.subject_repo.delete_for_user(subj)

    def add_unit(self, subject_id: str, user_id: str, data: UnitCreate) -> Unit:
        subj = self.get_subject(subject_id, user_id)
        unit = self.subject_repo.add_unit(subj.id, data.title, data.description, data.order_index)
        if data.topics:
            for t in data.topics:
                self.subject_repo.add_topic(
                    unit_id=unit.id,
                    title=t.title,
                    description=t.description,
                    difficulty=t.difficulty,
                    estimated_minutes=t.estimated_minutes,
                    order_index=t.order_index
                )
        return unit

    def add_topic(self, unit_id: str, user_id: str, data: TopicCreate) -> Topic:
        # Verify unit belongs to user
        unit = self.db.query(Unit).join(Subject).filter(Unit.id == unit_id, Subject.user_id == user_id).first()
        if not unit:
            raise ResourceNotFoundException("Unit not found or access denied.")
        return self.subject_repo.add_topic(
            unit_id=unit.id,
            title=data.title,
            description=data.description,
            difficulty=data.difficulty,
            estimated_minutes=data.estimated_minutes,
            order_index=data.order_index
        )
