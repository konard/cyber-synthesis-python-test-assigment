"""Post model with 4 different content types."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class PostType(str, Enum):
    """Types of posts (4 different content models)."""

    STANDARD = "standard"  # Regular post with text/media
    PAID = "paid"  # Paid content linked to billing
    EVENT = "event"  # Event-linked post
    MARKETPLACE = "marketplace"  # Marketplace listing


class PostStatus(str, Enum):
    """Post moderation status."""

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    PUBLISHED = "published"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Post(Base):
    """Post model for feed content with geolocation support."""

    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    author_id: Mapped[str] = mapped_column(String(36), index=True)
    post_type: Mapped[str] = mapped_column(String(20), default=PostType.STANDARD)
    status: Mapped[str] = mapped_column(String(20), default=PostStatus.PUBLISHED)

    # Content
    title: Mapped[str | None] = mapped_column(String(200))
    content: Mapped[str | None] = mapped_column(Text)
    media_urls: Mapped[list[str] | None] = mapped_column(ARRAY(String(500)))
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(50)))

    # Geolocation (optional for map display)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    location_name: Mapped[str | None] = mapped_column(String(200))

    # Type-specific data
    metadata: Mapped[dict | None] = mapped_column(JSONB)

    # For paid posts
    price: Mapped[float | None] = mapped_column(Float)
    currency: Mapped[str | None] = mapped_column(String(3))

    # For event posts
    event_id: Mapped[str | None] = mapped_column(String(36))

    # For marketplace
    is_sold: Mapped[bool] = mapped_column(Boolean, default=False)

    # Engagement counters
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)
    views_count: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        """String representation of Post."""
        return f"<Post(id={self.id}, type={self.post_type}, author={self.author_id})>"
