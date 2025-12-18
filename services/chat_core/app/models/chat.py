"""Chat model for 1-to-1 conversations."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base


class Chat(Base):
    """Chat model for 1-to-1 conversations."""

    __tablename__ = "chats"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user1_id: Mapped[str] = mapped_column(String(36), index=True)
    user2_id: Mapped[str] = mapped_column(String(36), index=True)

    # Reference to the match that created this chat
    match_id: Mapped[str | None] = mapped_column(String(36))

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user1_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    user2_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of Chat."""
        return f"<Chat(id={self.id}, user1={self.user1_id}, user2={self.user2_id})>"


# Avoid circular import
from services.chat_core.app.models.message import Message  # noqa: E402
