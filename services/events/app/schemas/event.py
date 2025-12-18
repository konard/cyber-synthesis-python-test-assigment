"""Event schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EventCreate(BaseModel):
    """Schema for creating an event."""

    title: str
    description: str | None = None
    cover_image_url: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    start_datetime: datetime
    end_datetime: datetime | None = None
    timezone: str = "UTC"
    is_online: bool = False
    location_name: str | None = None
    location_address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    online_url: str | None = None
    max_attendees: int | None = None
    settings: dict[str, Any] | None = None


class EventUpdate(BaseModel):
    """Schema for updating an event."""

    title: str | None = None
    description: str | None = None
    cover_image_url: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    timezone: str | None = None
    is_online: bool | None = None
    location_name: str | None = None
    location_address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    online_url: str | None = None
    max_attendees: int | None = None
    is_published: bool | None = None
    is_cancelled: bool | None = None
    settings: dict[str, Any] | None = None


class EventResponse(BaseModel):
    """Schema for event response."""

    id: str
    organizer_id: str
    title: str
    description: str | None = None
    cover_image_url: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    start_datetime: datetime
    end_datetime: datetime | None = None
    timezone: str
    is_online: bool
    location_name: str | None = None
    location_address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    online_url: str | None = None
    max_attendees: int | None = None
    current_attendees: int = 0
    is_published: bool = False
    is_cancelled: bool = False
    feed_post_id: str | None = None
    settings: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
