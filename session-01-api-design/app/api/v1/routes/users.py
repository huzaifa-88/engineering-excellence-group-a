from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.deps import get_db
from app.schemas.user import UserCreate, UserListResponse, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Registers a new user in the system after validating email and username uniqueness.",
)
async def create_user(
    payload: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
) -> UserResponse:
    """POST /users - Create a new user."""
    user = await UserService.create_user(db, payload)
    response.headers["location"] = f"/users/{user.id}"
    return UserResponse.model_validate(user)


@router.get(
    "",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
    summary="List users",
    description="Retrieve a paginated list of users.",
)
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    offset: int = Query(default=0, ge=0, description="Offset starting position"),
) -> UserListResponse:
    """GET /users - Paginated user list."""
    page = (offset // limit) + 1 if limit > 0 else 1
    users, total = await UserService.get_users(db, limit=limit, offset=offset)
    return UserListResponse(
        items=[UserResponse.model_validate(u) for u in users],
        page=page,
        page_size=limit,
        total=total,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Fetch details for a specific user by UUID.",
)
async def get_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """GET /users/{user_id} - Retrieve user by UUID."""
    user = await UserService.get_user(db, user_id)
    return UserResponse.model_validate(user)