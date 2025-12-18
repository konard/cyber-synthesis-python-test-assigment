"""Ticket model for event tickets."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class TicketStatus(str, Enum):
    """Ticket status states."""

    ACTIVE = "active"
    USED = "used"
    GIFTED = "gifted"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Ticket(Base):
    """Ticket model for event attendance."""

    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.id"), index=True
    )
    owner_id: Mapped[str] = mapped_column(String(36), index=True)
    original_owner_id: Mapped[str] = mapped_column(String(36))

    # Status
    status: Mapped[str] = mapped_column(String(20), default=TicketStatus.ACTIVE)

    # For gifted tickets
    gifted_to_id: Mapped[str | None] = mapped_column(String(36))
    gifted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Usage
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Transaction reference
    transaction_id: Mapped[str | None] = mapped_column(String(36))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        """String representation of Ticket."""
        return f"<Ticket(id={self.id}, event={self.event_id}, status={self.status})>"
