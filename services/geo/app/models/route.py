"""Route model for user tracks (LINESTRING)."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class Route(Base):
    """Route model - track as LINESTRING for PostGIS.

    In production, uses PostGIS geometry types for efficient
    spatial operations like ST_Intersects.
    """

    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), index=True)

    # Route name and description
    name: Mapped[str | None] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)

    # Route data as array of coordinates [[lat, lng], ...]
    # In production, this would be a PostGIS LINESTRING geometry
    coordinates: Mapped[list | None] = mapped_column(JSONB)

    # Route metadata
    distance_meters: Mapped[float | None] = mapped_column(Float)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    elevation_gain_meters: Mapped[float | None] = mapped_column(Float)

    # Bounding box for quick filtering
    min_lat: Mapped[float | None] = mapped_column(Float)
    max_lat: Mapped[float | None] = mapped_column(Float)
    min_lng: Mapped[float | None] = mapped_column(Float)
    max_lng: Mapped[float | None] = mapped_column(Float)

    # Activity type
    activity_type: Mapped[str | None] = mapped_column(String(50))

    # Privacy
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        """String representation of Route."""
        return f"<Route(id={self.id}, user={self.user_id})>"
