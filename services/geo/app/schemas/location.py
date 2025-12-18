"""Location schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class LocationUpdate(BaseModel):
    """Schema for updating user location."""

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accuracy_meters: float | None = None
    altitude_meters: float | None = None
    heading: float | None = None
    speed_mps: float | None = None
    is_invisible: bool | None = None
    share_with_matches_only: bool | None = None


class LocationResponse(BaseModel):
    """Schema for location response."""

    id: str
    user_id: str
    latitude: float
    longitude: float
    accuracy_meters: float | None = None
    is_invisible: bool = False
    share_with_matches_only: bool = True
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class NearbyUserResponse(BaseModel):
    """Schema for nearby user response."""

    user_id: str
    latitude: float
    longitude: float
    distance_meters: float
    updated_at: datetime
