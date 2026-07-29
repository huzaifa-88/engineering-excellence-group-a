from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.deps import PaginationParams, get_db
from app.schemas.task import (
    TaskCreate,
    TaskListResponse,
    TaskPriorityValue,
    TaskResponse,
    TaskStatusUpdate,
    TaskStatusValue,
)
from app.services.task_service import TaskService, to_task_response

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a task under a project. Validates project and optional assignee.",
)
async def create_task(
    payload: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
) -> TaskResponse:
    """POST /tasks - Create a new task."""
    task = await TaskService.create_task(db, payload)
    response.headers["location"] = f"/tasks/{task.id}"
    return to_task_response(task)


@router.get(
    "",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="List tasks",
    description="Paginated task list with optional status, priority, project, and assignee filters.",
)
async def list_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: PaginationParams = Depends(),
    status_filter: TaskStatusValue | None = Query(
        default=None,
        alias="status",
        description="Filter by status: todo | in_progress | done",
    ),
    priority: TaskPriorityValue | None = Query(
        default=None,
        description="Filter by priority: low | medium | high",
    ),
    project_id: UUID | None = Query(default=None, description="Filter by project"),
    assignee_id: UUID | None = Query(default=None, description="Filter by assignee"),
) -> TaskListResponse:
    """GET /tasks - Paginated and filtered task list."""
    tasks, total = await TaskService.get_tasks(
        db,
        page=pagination.page,
        page_size=pagination.page_size,
        status=status_filter,
        priority=priority,
        project_id=project_id,
        assignee_id=assignee_id,
    )
    return TaskListResponse(
        items=[to_task_response(t) for t in tasks],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Fetch a single task by UUID. Returns 404 if missing.",
)
async def get_task(
    task_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """GET /tasks/{task_id} - Retrieve one task."""
    task = await TaskService.get_task(db, task_id)
    return to_task_response(task)


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task status",
    description="Updates only the task status. Returns 404 if the task does not exist.",
)
async def update_task_status(
    task_id: UUID,
    payload: TaskStatusUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """PATCH /tasks/{task_id}/status - Update task status."""
    task = await TaskService.update_task_status(db, task_id, payload)
    return to_task_response(task)
