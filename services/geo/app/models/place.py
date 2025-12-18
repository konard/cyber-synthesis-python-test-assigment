"""Place model for points of interest."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class Place(Base):
    """Place model - static points of interest."""

    __tablename__ = "places"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    # Basic info
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50))
    subcategory: Mapped[str | None] = mapped_column(String(50))
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(50)))

    # Location
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float, index=True)
    address: Mapped[str | None] = mapped_column(String(500))
    city: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(100))

    # Media
    photo_urls: Mapped[list[str] | None] = mapped_column(ARRAY(String(500)))

    # External reference (for cached API results)
    external_id: Mapped[str | None] = mapped_column(String(100))
    external_source: Mapped[str | None] = mapped_column(String(50))
    external_data: Mapped[dict | None] = mapped_column(JSONB)

    # Rating
    rating: Mapped[float | None] = mapped_column(Float)
    ratings_count: Mapped[int] = mapped_column(Integer, default=0)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Created by user (optional)
    created_by_user_id: Mapped[str | None] = mapped_column(String(36))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        """String representation of Place."""
        return f"<Place(id={self.id}, name={self.name})>"
