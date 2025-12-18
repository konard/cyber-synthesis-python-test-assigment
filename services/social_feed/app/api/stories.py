"""Story API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.social_feed.app.schemas.story import StoryCreate, StoryResponse
from services.social_feed.app.services.feed_service import FeedService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
async def create_story(
    story_data: StoryCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new story."""
    service = FeedService(db)
    return await service.create_story(current_user["sub"], story_data)


@router.get("/", response_model=list[StoryResponse])
async def get_stories(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get all active stories."""
    service = FeedService(db)
    return await service.get_active_stories()


@router.get("/me", response_model=list[StoryResponse])
async def get_my_stories(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's stories."""
    service = FeedService(db)
    return await service.get_active_stories(current_user["sub"])
