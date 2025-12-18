"""Event service for event management."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.events.app.models.event import Event
from services.events.app.models.ticket import Ticket, TicketStatus
from services.events.app.schemas.event import EventCreate, EventUpdate
from shared.messaging.events import EventType, ServiceEvent, event_bus


class EventService:
    """Service for event operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize event service."""
        self.db = db

    async def create_event(self, organizer_id: str, event_data: EventCreate) -> Event:
        """Create a new event."""
        event = Event(
            organizer_id=organizer_id,
            title=event_data.title,
            description=event_data.description,
            cover_image_url=event_data.cover_image_url,
            category=event_data.category,
            tags=event_data.tags,
            start_datetime=event_data.start_datetime,
            end_datetime=event_data.end_datetime,
            timezone=event_data.timezone,
            is_online=event_data.is_online,
            location_name=event_data.location_name,
            location_address=event_data.location_address,
            latitude=event_data.latitude,
            longitude=event_data.longitude,
            online_url=event_data.online_url,
            max_attendees=event_data.max_attendees,
            settings=event_data.settings,
        )
        self.db.add(event)
        await self.db.flush()

        # Publish event
        service_event = ServiceEvent(
            event_type=EventType.EVENT_CREATED,
            data={
                "event_id": event.id,
                "organizer_id": organizer_id,
                "title": event_data.title,
                "has_geo": event_data.latitude is not None,
            },
            source_service="events",
        )
        await event_bus.publish(service_event)

        return event

    async def get_event(self, event_id: str) -> Event | None:
        """Get event by ID."""
        result = await self.db.execute(select(Event).where(Event.id == event_id))
        return result.scalar_one_or_none()

    async def get_events(
        self, limit: int = 20, offset: int = 0, organizer_id: str | None = None
    ) -> list[Event]:
        """Get events."""
        query = select(Event).where(
            Event.is_published.is_(True), Event.is_cancelled.is_(False)
        )
        if organizer_id:
            query = query.where(Event.organizer_id == organizer_id)

        query = query.order_by(Event.start_datetime.asc()).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_upcoming_events(self, user_id: str) -> list[Event]:
        """Get upcoming events for a user's calendar."""
        now = datetime.now(timezone.utc)
        result = await self.db.execute(
            select(Event)
            .where(
                Event.start_datetime > now,
                Event.is_published.is_(True),
                Event.is_cancelled.is_(False),
            )
            .order_by(Event.start_datetime.asc())
        )
        return list(result.scalars().all())

    async def update_event(
        self, event_id: str, organizer_id: str, event_data: EventUpdate
    ) -> Event | None:
        """Update an event."""
        result = await self.db.execute(
            select(Event).where(
                Event.id == event_id, Event.organizer_id == organizer_id
            )
        )
        event = result.scalar_one_or_none()
        if not event:
            return None

        update_data = event_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)

        service_event = ServiceEvent(
            event_type=EventType.EVENT_UPDATED,
            data={"event_id": event.id, "organizer_id": organizer_id},
            source_service="events",
        )
        await event_bus.publish(service_event)

        return event

    async def create_ticket(self, event_id: str, user_id: str) -> Ticket | None:
        """Create a ticket for an event."""
        event = await self.get_event(event_id)
        if not event:
            return None

        if event.max_attendees and event.current_attendees >= event.max_attendees:
            return None

        ticket = Ticket(
            event_id=event_id,
            owner_id=user_id,
            original_owner_id=user_id,
        )
        self.db.add(ticket)
        event.current_attendees += 1
        await self.db.flush()

        service_event = ServiceEvent(
            event_type=EventType.TICKET_PURCHASED,
            data={
                "ticket_id": ticket.id,
                "event_id": event_id,
                "user_id": user_id,
            },
            source_service="events",
        )
        await event_bus.publish(service_event)

        return ticket

    async def get_user_tickets(self, user_id: str) -> list[Ticket]:
        """Get tickets for a user."""
        result = await self.db.execute(
            select(Ticket)
            .where(Ticket.owner_id == user_id)
            .order_by(Ticket.created_at.desc())
        )
        return list(result.scalars().all())

    async def gift_ticket(
        self, ticket_id: str, user_id: str, recipient_id: str
    ) -> Ticket | None:
        """Gift a ticket to another user."""
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.id == ticket_id,
                Ticket.owner_id == user_id,
                Ticket.status == TicketStatus.ACTIVE,
            )
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            return None

        ticket.status = TicketStatus.GIFTED
        ticket.gifted_to_id = recipient_id
        ticket.gifted_at = datetime.now(timezone.utc)

        # Create new ticket for recipient
        new_ticket = Ticket(
            event_id=ticket.event_id,
            owner_id=recipient_id,
            original_owner_id=ticket.original_owner_id,
        )
        self.db.add(new_ticket)
        await self.db.flush()

        return new_ticket

    async def use_ticket(self, ticket_id: str, user_id: str) -> Ticket | None:
        """Mark a ticket as used."""
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.id == ticket_id,
                Ticket.owner_id == user_id,
                Ticket.status == TicketStatus.ACTIVE,
            )
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            return None

        ticket.status = TicketStatus.USED
        ticket.used_at = datetime.now(timezone.utc)

        return ticket

    async def get_geo_events(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[Event]:
        """Get events near a location."""
        # Placeholder - in production use PostGIS ST_DWithin
        result = await self.db.execute(
            select(Event).where(
                Event.is_published.is_(True),
                Event.is_cancelled.is_(False),
                Event.latitude.isnot(None),
                Event.longitude.isnot(None),
            )
        )
        return list(result.scalars().all())
