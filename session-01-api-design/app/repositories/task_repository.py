from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskPriority, TaskStatus


class TaskRepository:
    """Repository handling database operations for the Task entity."""

    @staticmethod
    async def get_by_id(db: AsyncSession, task_id: UUID) -> Task | None:
        """Fetch task by UUID primary key."""
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
        *,
        limit: int = 10,
        offset: int = 0,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        project_id: UUID | None = None,
        assignee_id: UUID | None = None,
    ) -> tuple[list[Task], int]:
        """Fetch paginated list of tasks with optional filters."""
        query = select(Task)

        if status is not None:
            query = query.where(Task.status == status)
        if priority is not None:
            query = query.where(Task.priority == priority)
        if project_id is not None:
            query = query.where(Task.project_id == project_id)
        if assignee_id is not None:
            query = query.where(Task.assigned_to == assignee_id)

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar_one()

        result = await db.execute(query.offset(offset).limit(limit))
        tasks = list(result.scalars().all())
        return tasks, total

    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Task:
        """Create and persist a new task entity in the database."""
        task = Task(**kwargs)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def update_status(
        db: AsyncSession,
        task: Task,
        status: TaskStatus,
    ) -> Task:
        """Update only the status field on an existing task."""
        task.status = status
        await db.commit()
        await db.refresh(task)
        return task
