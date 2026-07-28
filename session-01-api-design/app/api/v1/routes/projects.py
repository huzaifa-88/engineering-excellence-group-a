from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.deps import SessionDep, PaginationParams
from app.models.project import ProjectStatus
from app.schemas.project import ProjectCreate, ProjectListResponse, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
async def create_project(
    payload: ProjectCreate,
    session: SessionDep,
):
    """
    Create a new project with the provided details.
    """
    project = await ProjectService.create_project(session, payload)

    return project


@router.get(
    "",
    response_model=ProjectListResponse,
    summary="List all projects",
)
async def list_projects(
    pagination: PaginationParams = Depends(),
    status: ProjectStatus | None = Query(None, description="Filter by status"),
    owner_id: UUID | None = Query(None, description="Filter by owner ID"),
    session: SessionDep = None, # type checker trick, injected by FastAPI
):
    """
    Retrieve a paginated list of projects. Optional filters by status and owner_id can be applied.
    """
    projects, total = await ProjectService.get_projects(
        session,
        page=pagination.page,
        page_size=pagination.page_size,
        status=status,
        owner_id=owner_id,
    )

    return ProjectListResponse(
        items=projects,
        page=pagination.page,
        page_size=pagination.page_size,
        total=total,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
)
async def get_project(
    project_id: UUID,
    session: SessionDep,
):
    """
    Retrieve a specific project by its ID.
    """
    project = await ProjectService.get_project(session, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project
