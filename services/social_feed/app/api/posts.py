"""Post API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.social_feed.app.schemas.comment import CommentCreate, CommentResponse
from services.social_feed.app.schemas.post import PostCreate, PostResponse, PostUpdate
from services.social_feed.app.services.feed_service import FeedService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new post."""
    service = FeedService(db)
    return await service.create_post(current_user["sub"], post_data)


@router.get("/feed", response_model=list[PostResponse])
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get feed for current user."""
    service = FeedService(db)
    return await service.get_feed(current_user["sub"], limit, offset)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get post by ID."""
    service = FeedService(db)
    post = await service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update a post."""
    service = FeedService(db)
    post = await service.update_post(post_id, current_user["sub"], post_data)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a post."""
    service = FeedService(db)
    if not await service.delete_post(post_id, current_user["sub"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
async def like_post(
    post_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Like a post."""
    service = FeedService(db)
    if not await service.like_post(post_id, current_user["sub"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already liked"
        )
    return {"success": True}


@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_post(
    post_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Unlike a post."""
    service = FeedService(db)
    if not await service.unlike_post(post_id, current_user["sub"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not liked")


@router.post(
    "/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_comment(
    post_id: str,
    comment_data: CommentCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Add a comment to a post."""
    comment_data.post_id = post_id
    service = FeedService(db)
    comment = await service.add_comment(current_user["sub"], comment_data)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return comment


@router.get("/{post_id}/comments", response_model=list[CommentResponse])
async def get_comments(
    post_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get comments for a post."""
    service = FeedService(db)
    return await service.get_comments(post_id, limit, offset)


@router.get("/geo/nearby", response_model=list[PostResponse])
async def get_geo_posts(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(10, ge=1, le=100),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get posts near a location."""
    service = FeedService(db)
    return await service.get_geo_posts(latitude, longitude, radius_km)
