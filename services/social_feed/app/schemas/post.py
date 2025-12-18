"""Post schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.social_feed.app.models.post import PostType


class PostCreate(BaseModel):
    """Schema for creating a post."""

    post_type: PostType = PostType.STANDARD
    title: str | None = None
    content: str | None = None
    media_urls: list[str] | None = None
    tags: list[str] | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_name: str | None = None
    metadata: dict[str, Any] | None = None
    price: float | None = Field(None, ge=0)
    currency: str | None = Field(None, max_length=3)
    event_id: str | None = None


class PostUpdate(BaseModel):
    """Schema for updating a post."""

    title: str | None = None
    content: str | None = None
    media_urls: list[str] | None = None
    tags: list[str] | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_name: str | None = None
    metadata: dict[str, Any] | None = None
    price: float | None = None
    is_sold: bool | None = None


class PostResponse(BaseModel):
    """Schema for post response."""

    id: str
    author_id: str
    post_type: str
    status: str
    title: str | None = None
    content: str | None = None
    media_urls: list[str] | None = None
    tags: list[str] | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_name: str | None = None
    metadata: dict[str, Any] | None = None
    price: float | None = None
    currency: str | None = None
    event_id: str | None = None
    is_sold: bool = False
    likes_count: int = 0
    comments_count: int = 0
    views_count: int = 0
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True
