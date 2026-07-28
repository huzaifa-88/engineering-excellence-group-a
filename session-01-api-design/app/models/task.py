from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, UUID, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
import enum


class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class TaskPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class Task(Base):
    __tablename__ = "task"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"))
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
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
