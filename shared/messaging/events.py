"""Event bus for inter-service communication."""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class EventType(str, Enum):
    """Types of events in the system."""

    # Auth-Match events
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    MATCH_CREATED = "match.created"
    INVITATION_SENT = "invitation.sent"

    # Chat events
    MESSAGE_SENT = "message.sent"
    CHAT_CREATED = "chat.created"

    # Social-Feed events
    POST_CREATED = "post.created"
    POST_LIKED = "post.liked"
    COMMENT_ADDED = "comment.added"

    # Events service events
    EVENT_CREATED = "event.created"
    EVENT_UPDATED = "event.updated"
    TICKET_PURCHASED = "ticket.purchased"

    # Geo events
    LOCATION_UPDATED = "location.updated"
    ROUTE_RECORDED = "route.recorded"

    # Gamification events
    BALANCE_UPDATED = "balance.updated"
    REWARD_EARNED = "reward.earned"
    RATING_CHANGED = "rating.changed"


@dataclass
class ServiceEvent:
    """Event for inter-service communication."""

    event_type: EventType
    data: dict[str, Any]
    source_service: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_json(self) -> str:
        """Serialize event to JSON.

        Returns:
            JSON string representation
        """
        return json.dumps(
            {
                "event_id": self.event_id,
                "event_type": self.event_type.value,
                "data": self.data,
                "source_service": self.source_service,
                "timestamp": self.timestamp.isoformat(),
            }
        )

    @classmethod
    def from_json(cls, json_str: str) -> ServiceEvent:
        """Deserialize event from JSON.

        Args:
            json_str: JSON string to parse

        Returns:
            ServiceEvent instance
        """
        data = json.loads(json_str)
        return cls(
            event_id=data["event_id"],
            event_type=EventType(data["event_type"]),
            data=data["data"],
            source_service=data["source_service"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


EventHandler = Callable[[ServiceEvent], Coroutine[Any, Any, None]]


class EventBus:
    """Simple event bus for inter-service communication.

    In production, this would be replaced with Redis Pub/Sub,
    RabbitMQ, or Kafka.
    """

    def __init__(self) -> None:
        """Initialize the event bus."""
        self._handlers: dict[EventType, list[EventHandler]] = {}
        self._redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Subscribe to an event type.

        Args:
            event_type: Type of event to subscribe to
            handler: Async function to handle the event
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: ServiceEvent) -> None:
        """Publish an event to all subscribers.

        Args:
            event: Event to publish
        """
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            await handler(event)

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Unsubscribe from an event type.

        Args:
            event_type: Type of event to unsubscribe from
            handler: Handler to remove
        """
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type] if h != handler
            ]


# Global event bus instance
event_bus = EventBus()
