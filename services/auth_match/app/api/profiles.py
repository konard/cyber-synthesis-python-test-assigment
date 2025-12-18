"""Profile API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_match.app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from services.auth_match.app.services.user_service import UserService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's profile.

    Args:
        current_user: Current user from token
        db: Database session

    Returns:
        User profile
    """
    service = UserService(db)
    profile = await service.get_profile(current_user["sub"])
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.post("/me", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_my_profile(
    profile_data: ProfileCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create or update current user's profile.

    Args:
        profile_data: Profile data
        current_user: Current user from token
        db: Database session

    Returns:
        Created or updated profile
    """
    service = UserService(db)
    profile = await service.create_profile(current_user["sub"], profile_data)
    return profile


@router.patch("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update current user's profile.

    Args:
        profile_data: Profile update data
        current_user: Current user from token
        db: Database session

    Returns:
        Updated profile
    """
    service = UserService(db)
    profile = await service.update_profile(current_user["sub"], profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_user_profile(
    user_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get user profile by ID.

    Args:
        user_id: User ID
        current_user: Current user from token (for authorization)
        db: Database session

    Returns:
        User profile
    """
    service = UserService(db)
    profile = await service.get_profile(user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile
