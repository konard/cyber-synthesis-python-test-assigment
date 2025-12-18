"""Pydantic schemas for Geo service."""

from __future__ import annotations

from services.geo.app.schemas.location import LocationUpdate, LocationResponse
from services.geo.app.schemas.place import PlaceCreate, PlaceResponse
from services.geo.app.schemas.route import RouteCreate, RouteResponse

__all__ = [
    "LocationUpdate",
    "LocationResponse",
    "PlaceCreate",
    "PlaceResponse",
    "RouteCreate",
    "RouteResponse",
]
