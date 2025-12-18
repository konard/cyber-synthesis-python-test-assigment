"""Match and invitation schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.auth_match.app.models.match import InvitationType


class InvitationCreate(BaseModel):
    """Schema for creating an invitation."""

    recipient_id: str
    invitation_type: InvitationType
    message: str | None = None
    context_data: dict[str, Any] | None = None
    event_id: str | None = None  # Required for event invitations


class InvitationResponse(BaseModel):
    """Schema for invitation response."""

    id: str
    sender_id: str
    recipient_id: str
    invitation_type: str
    status: str
    message: str | None = None
    context_data: dict[str, Any] | None = None
    event_id: str | None = None
    created_at: datetime
    responded_at: datetime | None = None
    expires_at: datetime | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class InvitationAction(BaseModel):
    """Schema for responding to an invitation."""

    action: str = Field(..., pattern="^(accept|decline)$")


class MatchResponse(BaseModel):
    """Schema for match response."""

    id: str
    user1_id: str
    user2_id: str
    match_type: str
    is_active: bool
    created_at: datetime
    unmatched_at: datetime | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True
