"""Ticket schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TicketCreate(BaseModel):
    """Schema for creating a ticket."""

    event_id: str


class TicketGift(BaseModel):
    """Schema for gifting a ticket."""

    recipient_id: str


class TicketResponse(BaseModel):
    """Schema for ticket response."""

    id: str
    event_id: str
    owner_id: str
    original_owner_id: str
    status: str
    gifted_to_id: str | None = None
    gifted_at: datetime | None = None
    used_at: datetime | None = None
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
