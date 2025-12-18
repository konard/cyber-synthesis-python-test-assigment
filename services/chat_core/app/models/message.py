"""Message model for chat communications."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base

if TYPE_CHECKING:
    from services.chat_core.app.models.chat import Chat


class MessageType(str, Enum):
    """Types of messages."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"
    LOCATION = "location"
    QUICK_ACTION = "quick_action"  # Structured event from quick action panel
    SYSTEM = "system"


class QuickAction(str, Enum):
    """Quick action types from the chat panel (4 buttons)."""

    PROPOSE_MEETING = "propose_meeting"
    SHARE_LOCATION = "share_location"
    CREATE_EVENT = "create_event"
    SEND_GIFT = "send_gift"


class Message(Base):
    """Message model for chat communications."""

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    chat_id: Mapped[str] = mapped_column(String(36), ForeignKey("chats.id"), index=True)
    sender_id: Mapped[str] = mapped_column(String(36), index=True)

    # Message content
    message_type: Mapped[str] = mapped_column(String(20), default=MessageType.TEXT)
    content: Mapped[str | None] = mapped_column(Text)

    # For structured messages (quick actions, etc.)
    structured_data: Mapped[dict | None] = mapped_column(JSONB)

    # For media messages
    media_url: Mapped[str | None] = mapped_column(String(500))
    media_thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    media_metadata: Mapped[dict | None] = mapped_column(JSONB)

    # Quick action reference
    quick_action_type: Mapped[str | None] = mapped_column(String(30))

    # Status
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    edited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

    def __repr__(self) -> str:
        """String representation of Message."""
        return f"<Message(id={self.id}, type={self.message_type}, chat={self.chat_id})>"
