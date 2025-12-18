"""Subscription model for premium tiers."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class SubscriptionTier(str, Enum):
    """Subscription tiers."""

    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    VIP = "vip"


class Subscription(Base):
    """User subscription for premium features."""

    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    tier: Mapped[str] = mapped_column(String(20), default=SubscriptionTier.FREE)

    # Pricing
    price_monthly: Mapped[float | None] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)

    # Payment gateway reference
    external_subscription_id: Mapped[str | None] = mapped_column(String(100))

    # Features
    features: Mapped[dict | None] = mapped_column(JSONB)

    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        """String representation of Subscription."""
        return f"<Subscription(user={self.user_id}, tier={self.tier})>"
