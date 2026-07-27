from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, UUID, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
import enum


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    __tablename__ = "task"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    estimated_time = Column(Integer, nullable=True)  # in hours
    deadline = Column(DateTime, nullable=True)

    # Relationships
    project = relationship(
        "Project",
        back_populates="tasks",
    )
    assigned_to_user = relationship(
        "User",
        back_populates="assigned_tasks",
        foreign_keys=[assigned_to],
    )
    created_by_user = relationship(
        "User",
        back_populates="created_tasks",
        foreign_keys=[assigned_by],
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
