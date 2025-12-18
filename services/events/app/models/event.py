"""Event model for event management."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class Event(Base):
    """Event model for CRUD operations and calendar."""

    __tablename__ = "events"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    organizer_id: Mapped[str] = mapped_column(String(36), index=True)

    # Basic info
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    category: Mapped[str | None] = mapped_column(String(50))
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(50)))

    # Date/time
    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_datetime: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")

    # Location
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    location_name: Mapped[str | None] = mapped_column(String(200))
    location_address: Mapped[str | None] = mapped_column(String(500))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    online_url: Mapped[str | None] = mapped_column(String(500))

    # Capacity
    max_attendees: Mapped[int | None] = mapped_column(Integer)
    current_attendees: Mapped[int] = mapped_column(Integer, default=0)

    # Status
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Linked post in Social-Feed
    feed_post_id: Mapped[str | None] = mapped_column(String(36))

    # Settings
    settings: Mapped[dict | None] = mapped_column(JSONB)

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
        """String representation of Event."""
        return f"<Event(id={self.id}, title={self.title})>"
