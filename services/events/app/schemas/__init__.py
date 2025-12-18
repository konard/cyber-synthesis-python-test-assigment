"""Pydantic schemas for Events service."""

from __future__ import annotations

from services.events.app.schemas.event import EventCreate, EventResponse, EventUpdate
from services.events.app.schemas.ticket import TicketCreate, TicketResponse

__all__ = [
    "EventCreate",
    "EventResponse",
    "EventUpdate",
    "TicketCreate",
    "TicketResponse",
]
