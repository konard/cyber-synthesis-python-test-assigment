"""User location model for real-time tracking."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class UserLocation(Base):
    """User location model - point on map."""

    __tablename__ = "user_locations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)

    # Coordinates
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    # Accuracy
    accuracy_meters: Mapped[float | None] = mapped_column(Float)
    altitude_meters: Mapped[float | None] = mapped_column(Float)
    heading: Mapped[float | None] = mapped_column(Float)
    speed_mps: Mapped[float | None] = mapped_column(Float)

    # Privacy settings
    is_invisible: Mapped[bool] = mapped_column(Boolean, default=False)
    share_with_matches_only: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        """String representation of UserLocation."""
        return f"<UserLocation(user={self.user_id}, lat={self.latitude}, lng={self.longitude})>"
