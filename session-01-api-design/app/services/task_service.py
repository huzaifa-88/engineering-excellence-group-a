from __future__ import annotations

from uuid import UUID

from app.core.exceptions import (
    AssigneeNotFoundError,
    ProjectNotFoundError,
    TaskNotFoundError,
)
from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task import (
    TaskCreate,
    TaskPriorityValue,
    TaskResponse,
    TaskStatusUpdate,
    TaskStatusValue,
)
from sqlalchemy.ext.asyncio import AsyncSession

# API uses lowercase REST values; DB enums stay UPPERCASE (existing migrations).
_STATUS_TO_MODEL = {
    TaskStatusValue.TODO: TaskStatus.TODO,
    TaskStatusValue.IN_PROGRESS: TaskStatus.IN_PROGRESS,
    TaskStatusValue.DONE: TaskStatus.DONE,
}
_STATUS_TO_API = {v: k for k, v in _STATUS_TO_MODEL.items()}

_PRIORITY_TO_MODEL = {
    TaskPriorityValue.LOW: TaskPriority.LOW,
    TaskPriorityValue.MEDIUM: TaskPriority.MEDIUM,
    TaskPriorityValue.HIGH: TaskPriority.HIGH,
}
_PRIORITY_TO_API = {v: k for k, v in _PRIORITY_TO_MODEL.items()}


def to_task_response(task: Task) -> TaskResponse:
    """Map a Task ORM row to the public API response shape."""
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=_PRIORITY_TO_API.get(task.priority, TaskPriorityValue.MEDIUM),
        status=_STATUS_TO_API.get(task.status, TaskStatusValue.TODO),
        project_id=task.project_id,
        assignee_id=task.assigned_to,
        estimated_time=task.estimated_time,
        deadline=task.deadline,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


class TaskService:
    """Business logic service layer for Task management."""

    @staticmethod
    async def create_task(db: AsyncSession, payload: TaskCreate) -> Task:
        """Create a new task after validating project and optional assignee."""
        project = await ProjectRepository.get_by_id(db, payload.project_id)
        if project is None:
            raise ProjectNotFoundError()

        if payload.assignee_id is not None:
            assignee = await UserRepository.get_by_id(db, payload.assignee_id)
            if assignee is None:
                raise AssigneeNotFoundError()

        data = {
            "title": payload.title,
            "description": payload.description,
            "priority": _PRIORITY_TO_MODEL[payload.priority],
            "status": _STATUS_TO_MODEL[payload.status],
            "project_id": payload.project_id,
            "assigned_to": payload.assignee_id,
            "estimated_time": payload.estimated_time,
            "deadline": payload.deadline,
        }

        # Strip timezone info to match DB column type (TIMESTAMP WITHOUT TIME ZONE)
        if data.get("deadline") and data["deadline"].tzinfo is not None:
            data["deadline"] = data["deadline"].replace(tzinfo=None)

        return await TaskRepository.create(db, **data)

    @staticmethod
    async def get_tasks(
        db: AsyncSession,
        *,
        page: int = 1,
        page_size: int = 10,
        status: TaskStatusValue | None = None,
        priority: TaskPriorityValue | None = None,
        project_id: UUID | None = None,
        assignee_id: UUID | None = None,
    ) -> tuple[list[Task], int]:
        """Fetch a paginated list of tasks with optional filters."""
        offset = (page - 1) * page_size
        return await TaskRepository.get_all(
            db,
            limit=page_size,
            offset=offset,
            status=_STATUS_TO_MODEL[status] if status else None,
            priority=_PRIORITY_TO_MODEL[priority] if priority else None,
            project_id=project_id,
            assignee_id=assignee_id,
        )

    @staticmethod
    async def get_task(db: AsyncSession, task_id: UUID) -> Task:
        """Fetch a task by UUID or raise TaskNotFoundError."""
        task = await TaskRepository.get_by_id(db, task_id)
        if task is None:
            raise TaskNotFoundError()
        return task

    @staticmethod
    async def update_task_status(
        db: AsyncSession,
        task_id: UUID,
        payload: TaskStatusUpdate,
    ) -> Task:
        """Update only the task status or raise TaskNotFoundError."""
        task = await TaskRepository.get_by_id(db, task_id)
        if task is None:
            raise TaskNotFoundError()

        return await TaskRepository.update_status(
            db,
            task,
            _STATUS_TO_MODEL[payload.status],
        )
