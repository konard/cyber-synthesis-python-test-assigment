"""Routes API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.geo.app.schemas.route import RouteCreate, RouteIntersection, RouteResponse
from services.geo.app.services.geo_service import GeoService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    route_data: RouteCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new route (track)."""
    service = GeoService(db)
    return await service.create_route(current_user["sub"], route_data)


@router.get("/", response_model=list[RouteResponse])
async def get_my_routes(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's routes."""
    service = GeoService(db)
    return await service.get_user_routes(current_user["sub"])


@router.get("/intersections/{route1_id}/{route2_id}", response_model=RouteIntersection)
async def get_route_intersections(
    route1_id: str,
    route2_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Find intersections between two routes."""
    service = GeoService(db)
    points = await service.find_route_intersections(route1_id, route2_id)
    return RouteIntersection(
        route1_id=route1_id,
        route2_id=route2_id,
        intersection_count=len(points),
        intersection_points=points if points else None,
    )
