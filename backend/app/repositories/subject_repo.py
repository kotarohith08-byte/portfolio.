"""
StudyChart AI - Subject Repository with Strict User Isolation.
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.subject import Subject, Unit, Topic, Subtopic, Resource
from app.schemas.subject import SubjectCreate, SubjectUpdate

class SubjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: str, include_archived: bool = False) -> List[Subject]:
        query = self.db.query(Subject).options(
            joinedload(Subject.units).joinedload(Unit.topics).joinedload(Topic.subtopics),
            joinedload(Subject.units).joinedload(Unit.topics).joinedload(Topic.resources)
        ).filter(Subject.user_id == user_id)

        if not include_archived:
            query = query.filter(Subject.is_archived == False)

        return query.order_by(Subject.priority.desc(), Subject.name.asc()).all()

    def get_by_id_for_user(self, subject_id: str, user_id: str) -> Optional[Subject]:
        return self.db.query(Subject).options(
            joinedload(Subject.units).joinedload(Unit.topics).joinedload(Topic.subtopics),
            joinedload(Subject.units).joinedload(Unit.topics).joinedload(Topic.resources)
        ).filter(Subject.id == subject_id, Subject.user_id == user_id).first()

    def create_for_user(self, user_id: str, data: SubjectCreate) -> Subject:
        subject = Subject(
            user_id=user_id,
            name=data.name.strip(),
            description=data.description,
            color=data.color,
            icon=data.icon,
            exam_date=data.exam_date,
            target_grade=data.target_grade,
            priority=data.priority
        )
        self.db.add(subject)
        self.db.commit()
        self.db.refresh(subject)
        return subject

    def update_for_user(self, subject: Subject, data: SubjectUpdate) -> Subject:
        if data.name is not None:
            subject.name = data.name.strip()
        if data.description is not None:
            subject.description = data.description
        if data.color is not None:
            subject.color = data.color
        if data.icon is not None:
            subject.icon = data.icon
        if data.exam_date is not None:
            subject.exam_date = data.exam_date
        if data.target_grade is not None:
            subject.target_grade = data.target_grade
        if data.priority is not None:
            subject.priority = data.priority
        if data.is_archived is not None:
            subject.is_archived = data.is_archived

        self.db.commit()
        self.db.refresh(subject)
        return subject

    def delete_for_user(self, subject: Subject) -> None:
        self.db.delete(subject)
        self.db.commit()

    def add_unit(self, subject_id: str, title: str, description: Optional[str] = None, order_index: int = 0) -> Unit:
        unit = Unit(
            subject_id=subject_id,
            title=title,
            description=description,
            order_index=order_index
        )
        self.db.add(unit)
        self.db.commit()
        self.db.refresh(unit)
        return unit

    def add_topic(self, unit_id: str, title: str, description: Optional[str] = None, difficulty: float = 3.0, estimated_minutes: int = 45, order_index: int = 0) -> Topic:
        topic = Topic(
            unit_id=unit_id,
            title=title,
            description=description,
            difficulty=difficulty,
            estimated_minutes=estimated_minutes,
            order_index=order_index
        )
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic
