"""Event API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.events.app.schemas.event import EventCreate, EventResponse, EventUpdate
from services.events.app.services.event_service import EventService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new event."""
    service = EventService(db)
    return await service.create_event(current_user["sub"], event_data)


@router.get("/", response_model=list[EventResponse])
async def get_events(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get events."""
    service = EventService(db)
    return await service.get_events(limit, offset)


@router.get("/upcoming", response_model=list[EventResponse])
async def get_upcoming_events(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get upcoming events for calendar."""
    service = EventService(db)
    return await service.get_upcoming_events(current_user["sub"])


@router.get("/me", response_model=list[EventResponse])
async def get_my_events(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get events organized by current user."""
    service = EventService(db)
    return await service.get_events(limit, offset, current_user["sub"])


@router.get("/geo/nearby", response_model=list[EventResponse])
async def get_geo_events(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(10, ge=1, le=100),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get events near a location."""
    service = EventService(db)
    return await service.get_geo_events(latitude, longitude, radius_km)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get event by ID."""
    service = EventService(db)
    event = await service.get_event(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    event_data: EventUpdate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update an event."""
    service = EventService(db)
    event = await service.update_event(event_id, current_user["sub"], event_data)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event
