from __future__ import annotations

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, DateTime, String, UUID, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProjectStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"


class Project(Base):
    __tablename__ = "project"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.ACTIVE)
    deadline = Column(DateTime, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    owner = relationship(
        "User",
        back_populates="owned_projects",
        foreign_keys=[owner_id],
    )
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    members = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, title={self.title}, status={self.status})>"
