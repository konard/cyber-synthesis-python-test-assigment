"""API routes for Geo service."""

from __future__ import annotations

from fastapi import APIRouter

from services.geo.app.api.locations import router as locations_router
from services.geo.app.api.places import router as places_router
from services.geo.app.api.routes import router as routes_router

router = APIRouter()
router.include_router(locations_router, prefix="/locations", tags=["locations"])
router.include_router(places_router, prefix="/places", tags=["places"])
router.include_router(routes_router, prefix="/routes", tags=["routes"])

__all__ = ["router"]
