"""Story model for ephemeral content."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class Story(Base):
    """Story model for ephemeral content (24-hour expiration).

    Requires virtual currency (SuperSignal) to publish.
    """

    __tablename__ = "stories"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    author_id: Mapped[str] = mapped_column(String(36), index=True)

    # Media
    media_url: Mapped[str] = mapped_column(String(500))
    media_type: Mapped[str] = mapped_column(String(10))  # 'image' or 'video'
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))

    # Optional text overlay
    text_overlay: Mapped[str | None] = mapped_column(String(500))
    text_style: Mapped[dict | None] = mapped_column(JSONB)

    # Geolocation
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    location_name: Mapped[str | None] = mapped_column(String(200))

    # Stats
    views_count: Mapped[int] = mapped_column(Integer, default=0)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Cost tracking
    cost_in_currency: Mapped[float] = mapped_column(Float, default=1.0)
    transaction_id: Mapped[str | None] = mapped_column(String(36))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        """String representation of Story."""
        return f"<Story(id={self.id}, author={self.author_id})>"
