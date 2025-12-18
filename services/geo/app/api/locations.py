"""Location API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.geo.app.schemas.location import LocationResponse, LocationUpdate
from services.geo.app.services.geo_service import GeoService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.put("/me", response_model=LocationResponse)
async def update_my_location(
    location_data: LocationUpdate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update current user's location."""
    service = GeoService(db)
    return await service.update_location(current_user["sub"], location_data)


@router.get("/me", response_model=LocationResponse)
async def get_my_location(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's location."""
    service = GeoService(db)
    location = await service.get_location(current_user["sub"])
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )
    return location


@router.get("/nearby", response_model=list[LocationResponse])
async def get_nearby_users(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, ge=0.1, le=100),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get nearby users."""
    service = GeoService(db)
    return await service.get_nearby_users(
        current_user["sub"], latitude, longitude, radius_km
    )
