from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_log import ActivityLog
from app.models.notification import Notification
from app.models.task import Task, TaskStatus
from app.models.task_assignment_history import TaskAssignmentHistory
from app.models.task_status_history import TaskStatusHistory


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
        **filters,
    ) -> tuple[list[Task], int]:
        """Fetch paginated list of tasks with optional dynamic filters."""
        query = select(Task)

        # Dynamic filtering based on model attributes
        for key, value in filters.items():
            if value is not None and hasattr(Task, key):
                query = query.where(getattr(Task, key) == value)

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
    async def update(db: AsyncSession, task: Task, **kwargs) -> Task:
        """Update any attributes on an existing task entity dynamically."""
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def update_status(
        db: AsyncSession,
        task: Task,
        status: TaskStatus,
    ) -> Task:
        """Update status on an existing task (wraps generic update)."""
        return await TaskRepository.update(db, task, status=status)

    @staticmethod
    async def get_assignment_history(
        db: AsyncSession, task_id: UUID
    ) -> list[TaskAssignmentHistory]:
        """Fetch all assignment history entries for a given task, ordered chronologically."""
        stmt = (
            select(TaskAssignmentHistory)
            .where(TaskAssignmentHistory.task_id == task_id)
            .order_by(TaskAssignmentHistory.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_status_history(
        db: AsyncSession, task_id: UUID
    ) -> list[TaskStatusHistory]:
        """Fetch all status history entries for a given task, ordered chronologically."""
        stmt = (
            select(TaskStatusHistory)
            .where(TaskStatusHistory.task_id == task_id)
            .order_by(TaskStatusHistory.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_activity_logs(db: AsyncSession, task_id: UUID) -> list[ActivityLog]:
        """Fetch all activity log records for a given task, ordered chronologically."""
        stmt = (
            select(ActivityLog)
            .where(ActivityLog.task_id == task_id)
            .order_by(ActivityLog.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_notifications(db: AsyncSession, task_id: UUID) -> list[Notification]:
        """Fetch all notifications related to a given task."""
        stmt = (
            select(Notification)
            .where(Notification.task_id == task_id)
            .order_by(Notification.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())
