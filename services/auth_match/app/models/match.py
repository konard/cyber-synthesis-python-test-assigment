"""Match and invitation models for pair interactions."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class InvitationType(str, Enum):
    """Types of user interaction invitations (4 types from swipe context menu)."""

    LIKE = "like"  # Standard like/match request
    EVENT_INVITE = "event_invite"  # Invite to an event
    CHAT_REQUEST = "chat_request"  # Request to start a chat
    ACTIVITY_PROPOSAL = "activity_proposal"  # Propose a joint activity


class InvitationStatus(str, Enum):
    """Status of an invitation."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


class Invitation(Base):
    """Invitation model for user interactions.

    Each swipe action creates a specific invitation object based on
    the selected action type from the context menu.
    """

    __tablename__ = "invitations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    sender_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    recipient_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    invitation_type: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(20), default=InvitationStatus.PENDING)

    # Context data for the invitation
    message: Mapped[str | None] = mapped_column(Text)
    context_data: Mapped[dict | None] = mapped_column(JSONB)

    # For event invitations - reference to the event
    event_id: Mapped[str | None] = mapped_column(String(36))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        """String representation of Invitation."""
        return (
            f"<Invitation(id={self.id}, type={self.invitation_type}, "
            f"sender={self.sender_id}, recipient={self.recipient_id})>"
        )


class Match(Base):
    """Match model for mutual interactions.

    A match is created when both users have mutually accepted invitations.
    """

    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user1_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    user2_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    # The invitation that triggered the match
    original_invitation_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("invitations.id")
    )

    # Match metadata
    match_type: Mapped[str] = mapped_column(String(30), default="mutual_like")
    is_active: Mapped[bool] = mapped_column(default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    unmatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        """String representation of Match."""
        return f"<Match(id={self.id}, user1={self.user1_id}, user2={self.user2_id})>"
