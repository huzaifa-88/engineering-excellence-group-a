from __future__ import annotations

from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectStatus
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse


class ProjectService:
    """Business logic service layer for Project management."""

    @staticmethod
    async def create_project(db: AsyncSession, payload: ProjectCreate) -> Project:
        """Create a new project with the provided details."""
        data = payload.model_dump()

        # Strip timezone info to match DB column type (TIMESTAMP WITHOUT TIME ZONE)
        if data.get("deadline") and data["deadline"].tzinfo is not None:
            data["deadline"] = data["deadline"].replace(tzinfo=None)

        return await ProjectRepository.create(db, **data)

    @staticmethod
    async def get_projects(
        db: AsyncSession,
        *,
        page: int = 1,
        page_size: int = 10,
        status: ProjectStatus | None = None,
        owner_id: UUID | None = None,
    ) -> tuple[list[Project], int]:
        """Fetch a paginated list of projects with optional filters."""
        offset = (page - 1) * page_size
        status_value = status.value if status else None
        return await ProjectRepository.get_all(
            db,
            limit=page_size,
            offset=offset,
            status=status_value,
            owner_id=owner_id,
        )

    @staticmethod
    async def get_project(db: AsyncSession, project_id: UUID) -> Project | None:
        """Fetch a project by UUID or return None if not found."""
        return await ProjectRepository.get_by_id(db, project_id)