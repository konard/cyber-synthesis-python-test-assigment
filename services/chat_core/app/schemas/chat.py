"""Chat schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ChatCreate(BaseModel):
    """Schema for creating a chat."""

    user2_id: str
    match_id: str | None = None


class ChatResponse(BaseModel):
    """Schema for chat response."""

    id: str
    user1_id: str
    user2_id: str
    match_id: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_message_at: datetime | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True
