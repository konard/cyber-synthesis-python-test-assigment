"""User API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_match.app.schemas.user import UserResponse, UserUpdate
from services.auth_match.app.services.user_service import UserService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user information.

    Args:
        current_user: Current user from token
        db: Database session

    Returns:
        Current user
    """
    service = UserService(db)
    user = await service.get_user_by_id(current_user["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update current user.

    Args:
        user_data: User update data
        current_user: Current user from token
        db: Database session

    Returns:
        Updated user
    """
    service = UserService(db)
    user = await service.update_user(current_user["sub"], user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get user by ID.

    Args:
        user_id: User ID
        current_user: Current user from token (for authorization)
        db: Database session

    Returns:
        User
    """
    service = UserService(db)
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
