"""Story schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class StoryCreate(BaseModel):
    """Schema for creating a story."""

    media_url: str
    media_type: str
    thumbnail_url: str | None = None
    text_overlay: str | None = None
    text_style: dict[str, Any] | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_name: str | None = None


class StoryResponse(BaseModel):
    """Schema for story response."""

    id: str
    author_id: str
    media_url: str
    media_type: str
    thumbnail_url: str | None = None
    text_overlay: str | None = None
    text_style: dict[str, Any] | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_name: str | None = None
    views_count: int = 0
    is_active: bool = True
    created_at: datetime
    expires_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
