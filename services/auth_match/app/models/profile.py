"""User profile model with extended attributes."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base

if TYPE_CHECKING:
    from services.auth_match.app.models.user import User


class UserProfile(Base):
    """Extended user profile with 15+ additional attributes."""

    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), unique=True
    )

    # Basic info
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    display_name: Mapped[str | None] = mapped_column(String(100))
    bio: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    cover_photo_url: Mapped[str | None] = mapped_column(String(500))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    gender: Mapped[str | None] = mapped_column(String(20))

    # Location
    city: Mapped[str | None] = mapped_column(String(100))
    region: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(100))

    # Contact
    phone_number: Mapped[str | None] = mapped_column(String(20))
    website: Mapped[str | None] = mapped_column(String(500))

    # Multiple choice attributes (stored as arrays)
    interests: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)))
    languages: Mapped[list[str] | None] = mapped_column(ARRAY(String(50)))
    skills: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)))

    # Text lists
    hobbies: Mapped[list[str] | None] = mapped_column(ARRAY(String(200)))
    favorite_places: Mapped[list[str] | None] = mapped_column(ARRAY(String(200)))

    # Numeric attributes
    height_cm: Mapped[int | None] = mapped_column(Integer)
    search_radius_km: Mapped[int | None] = mapped_column(Integer, default=50)

    # Preferences (JSONB for flexibility)
    preferences: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    notification_settings: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    privacy_settings: Mapped[dict | None] = mapped_column(JSONB, default=dict)

    # Location coordinates for quick filtering
    last_known_latitude: Mapped[float | None] = mapped_column(Float)
    last_known_longitude: Mapped[float | None] = mapped_column(Float)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        """String representation of UserProfile."""
        return f"<UserProfile(id={self.id}, user_id={self.user_id})>"
