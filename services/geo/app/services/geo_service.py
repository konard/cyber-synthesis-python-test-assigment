"""Geo service for geospatial operations."""

from __future__ import annotations

import math

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.geo.app.models.location import UserLocation
from services.geo.app.models.place import Place
from services.geo.app.models.route import Route
from services.geo.app.schemas.location import LocationUpdate
from services.geo.app.schemas.place import PlaceCreate
from services.geo.app.schemas.route import RouteCreate
from shared.messaging.events import EventType, ServiceEvent, event_bus


class GeoService:
    """Service for geospatial operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize geo service."""
        self.db = db

    async def update_location(
        self, user_id: str, location_data: LocationUpdate
    ) -> UserLocation:
        """Update user location."""
        result = await self.db.execute(
            select(UserLocation).where(UserLocation.user_id == user_id)
        )
        location = result.scalar_one_or_none()

        if location:
            for field, value in location_data.model_dump(exclude_unset=True).items():
                setattr(location, field, value)
        else:
            location = UserLocation(
                user_id=user_id, **location_data.model_dump(exclude_unset=True)
            )
            self.db.add(location)

        await self.db.flush()

        event = ServiceEvent(
            event_type=EventType.LOCATION_UPDATED,
            data={
                "user_id": user_id,
                "latitude": location.latitude,
                "longitude": location.longitude,
            },
            source_service="geo",
        )
        await event_bus.publish(event)

        return location

    async def get_location(self, user_id: str) -> UserLocation | None:
        """Get user location."""
        result = await self.db.execute(
            select(UserLocation).where(UserLocation.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_nearby_users(
        self, user_id: str, latitude: float, longitude: float, radius_km: float
    ) -> list[UserLocation]:
        """Get users within radius.

        In production, this would use PostGIS ST_DWithin.
        """
        result = await self.db.execute(
            select(UserLocation).where(
                UserLocation.user_id != user_id,
                UserLocation.is_invisible.is_(False),
            )
        )
        locations = result.scalars().all()

        # Filter by distance (simplified - production uses PostGIS)
        nearby = []
        for loc in locations:
            distance = self._haversine_distance(
                latitude, longitude, loc.latitude, loc.longitude
            )
            if distance <= radius_km * 1000:
                nearby.append(loc)

        return nearby

    def _haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Calculate distance between two points in meters."""
        r = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return r * c

    async def create_place(self, user_id: str, place_data: PlaceCreate) -> Place:
        """Create a new place."""
        place = Place(
            created_by_user_id=user_id,
            **place_data.model_dump(),
        )
        self.db.add(place)
        await self.db.flush()
        return place

    async def get_places_nearby(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[Place]:
        """Get places within radius."""
        result = await self.db.execute(select(Place).where(Place.is_active.is_(True)))
        places = result.scalars().all()

        nearby = []
        for place in places:
            distance = self._haversine_distance(
                latitude, longitude, place.latitude, place.longitude
            )
            if distance <= radius_km * 1000:
                nearby.append(place)

        return nearby

    async def create_route(self, user_id: str, route_data: RouteCreate) -> Route:
        """Create a new route (track)."""
        # Calculate bounding box and distance
        coords = route_data.coordinates
        lats = [c[0] for c in coords]
        lngs = [c[1] for c in coords]

        total_distance = 0.0
        for i in range(1, len(coords)):
            total_distance += self._haversine_distance(
                coords[i - 1][0], coords[i - 1][1], coords[i][0], coords[i][1]
            )

        route = Route(
            user_id=user_id,
            name=route_data.name,
            description=route_data.description,
            coordinates=coords,
            activity_type=route_data.activity_type,
            is_public=route_data.is_public,
            started_at=route_data.started_at,
            ended_at=route_data.ended_at,
            distance_meters=total_distance,
            min_lat=min(lats),
            max_lat=max(lats),
            min_lng=min(lngs),
            max_lng=max(lngs),
        )

        if route_data.started_at and route_data.ended_at:
            route.duration_seconds = int(
                (route_data.ended_at - route_data.started_at).total_seconds()
            )

        self.db.add(route)
        await self.db.flush()

        event = ServiceEvent(
            event_type=EventType.ROUTE_RECORDED,
            data={
                "route_id": route.id,
                "user_id": user_id,
                "distance_meters": total_distance,
            },
            source_service="geo",
        )
        await event_bus.publish(event)

        return route

    async def get_user_routes(self, user_id: str) -> list[Route]:
        """Get routes for a user."""
        result = await self.db.execute(
            select(Route)
            .where(Route.user_id == user_id)
            .order_by(Route.created_at.desc())
        )
        return list(result.scalars().all())

    async def find_route_intersections(
        self, route1_id: str, route2_id: str
    ) -> list[list[float]]:
        """Find intersections between two routes.

        In production, this uses PostGIS ST_Intersects.
        """
        # Placeholder - production implementation uses PostGIS
        return []
