"""Ticket API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.events.app.schemas.ticket import TicketCreate, TicketGift, TicketResponse
from services.events.app.services.event_service import EventService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get a ticket for an event."""
    service = EventService(db)
    ticket = await service.create_ticket(ticket_data.event_id, current_user["sub"])
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create ticket (event not found or full)",
        )
    return ticket


@router.get("/", response_model=list[TicketResponse])
async def get_my_tickets(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's tickets."""
    service = EventService(db)
    return await service.get_user_tickets(current_user["sub"])


@router.post("/{ticket_id}/gift", response_model=TicketResponse)
async def gift_ticket(
    ticket_id: str,
    gift_data: TicketGift,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Gift a ticket to another user."""
    service = EventService(db)
    ticket = await service.gift_ticket(
        ticket_id, current_user["sub"], gift_data.recipient_id
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not gift ticket",
        )
    return ticket


@router.post("/{ticket_id}/use", response_model=TicketResponse)
async def use_ticket(
    ticket_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Use a ticket."""
    service = EventService(db)
    ticket = await service.use_ticket(ticket_id, current_user["sub"])
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not use ticket",
        )
    return ticket
