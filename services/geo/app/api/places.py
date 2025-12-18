"""Places API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.geo.app.schemas.place import PlaceCreate, PlaceResponse
from services.geo.app.services.geo_service import GeoService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
async def create_place(
    place_data: PlaceCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new place."""
    service = GeoService(db)
    return await service.create_place(current_user["sub"], place_data)


@router.get("/nearby", response_model=list[PlaceResponse])
async def get_nearby_places(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, ge=0.1, le=100),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get places near a location."""
    service = GeoService(db)
    return await service.get_places_nearby(latitude, longitude, radius_km)
