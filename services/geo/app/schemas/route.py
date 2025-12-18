"""Route schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RouteCreate(BaseModel):
    """Schema for creating a route."""

    name: str | None = None
    description: str | None = None
    coordinates: list[list[float]]  # [[lat, lng], ...]
    activity_type: str | None = None
    is_public: bool = False
    started_at: datetime | None = None
    ended_at: datetime | None = None


class RouteResponse(BaseModel):
    """Schema for route response."""

    id: str
    user_id: str
    name: str | None = None
    description: str | None = None
    coordinates: list[Any] | None = None
    distance_meters: float | None = None
    duration_seconds: int | None = None
    elevation_gain_meters: float | None = None
    activity_type: str | None = None
    is_public: bool = False
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class RouteIntersection(BaseModel):
    """Schema for route intersection result."""

    route1_id: str
    route2_id: str
    intersection_count: int
    intersection_points: list[list[float]] | None = None
