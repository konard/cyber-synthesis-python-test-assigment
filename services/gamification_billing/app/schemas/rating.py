"""Rating schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RatingResponse(BaseModel):
    """Schema for rating response."""

    id: str
    user_id: str
    score: float
    level: int
    posts_count: int = 0
    comments_count: int = 0
    likes_received: int = 0
    events_created: int = 0
    events_attended: int = 0
    matches_count: int = 0
    city: str | None = None
    region: str | None = None
    country: str | None = None
    stats: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry."""

    rank: int
    user_id: str
    score: float
    level: int


class LeaderboardResponse(BaseModel):
    """Schema for leaderboard response."""

    scope: str  # 'global', 'country', 'region', 'city'
    scope_value: str | None = None
    entries: list[LeaderboardEntry]
    total_count: int
