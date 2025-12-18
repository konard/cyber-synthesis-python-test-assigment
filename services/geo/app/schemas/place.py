"""Place schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PlaceCreate(BaseModel):
    """Schema for creating a place."""

    name: str
    description: str | None = None
    category: str
    subcategory: str | None = None
    tags: list[str] | None = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: str | None = None
    city: str | None = None
    country: str | None = None
    photo_urls: list[str] | None = None


class PlaceResponse(BaseModel):
    """Schema for place response."""

    id: str
    name: str
    description: str | None = None
    category: str
    subcategory: str | None = None
    tags: list[str] | None = None
    latitude: float
    longitude: float
    address: str | None = None
    city: str | None = None
    country: str | None = None
    photo_urls: list[str] | None = None
    external_id: str | None = None
    external_source: str | None = None
    rating: float | None = None
    ratings_count: int = 0
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
