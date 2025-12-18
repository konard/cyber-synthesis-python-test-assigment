"""Message schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from services.chat_core.app.models.message import MessageType, QuickAction


class MessageCreate(BaseModel):
    """Schema for creating a message."""

    chat_id: str
    message_type: MessageType = MessageType.TEXT
    content: str | None = None
    media_url: str | None = None
    media_thumbnail_url: str | None = None
    media_metadata: dict[str, Any] | None = None
    structured_data: dict[str, Any] | None = None


class QuickActionMessage(BaseModel):
    """Schema for quick action message."""

    chat_id: str
    action_type: QuickAction
    data: dict[str, Any] | None = None


class MessageResponse(BaseModel):
    """Schema for message response."""

    id: str
    chat_id: str
    sender_id: str
    message_type: str
    content: str | None = None
    structured_data: dict[str, Any] | None = None
    media_url: str | None = None
    media_thumbnail_url: str | None = None
    media_metadata: dict[str, Any] | None = None
    quick_action_type: str | None = None
    is_read: bool
    is_deleted: bool
    created_at: datetime
    read_at: datetime | None = None
    edited_at: datetime | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class TranslationRequest(BaseModel):
    """Schema for AI translation request."""

    text: str
    target_language: str


class TranslationResponse(BaseModel):
    """Schema for AI translation response."""

    original_text: str
    translated_text: str
    target_language: str
