from __future__ import annotations

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async database session for API routes."""
    async for session in get_async_session():
        yield session
