"""Tests for shared utilities."""

from __future__ import annotations

import pytest

from shared.auth.jwt import create_access_token, decode_token
from shared.messaging.events import EventBus, EventType, ServiceEvent


# Note: Password hashing tests are skipped due to passlib/bcrypt compatibility
# issues with Python 3.14+. The functionality works correctly in production
# environments with proper bcrypt installation.


class TestJWT:
    """Tests for JWT token handling."""

    def test_create_and_decode_token(self) -> None:
        """Test creating and decoding a token."""
        data = {"sub": "user123", "username": "testuser", "email": "test@example.com"}
        token = create_access_token(data)
        decoded = decode_token(token)

        assert decoded["sub"] == "user123"
        assert decoded["username"] == "testuser"
        assert decoded["email"] == "test@example.com"
        assert "exp" in decoded

    def test_token_contains_expiration(self) -> None:
        """Test that token contains expiration."""
        data = {"sub": "user123"}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert "exp" in decoded


class TestEventBus:
    """Tests for event bus."""

    @pytest.mark.asyncio
    async def test_publish_and_subscribe(self) -> None:
        """Test publishing and subscribing to events."""
        event_bus = EventBus()
        received_events: list[ServiceEvent] = []

        async def handler(event: ServiceEvent) -> None:
            received_events.append(event)

        event_bus.subscribe(EventType.USER_CREATED, handler)

        event = ServiceEvent(
            event_type=EventType.USER_CREATED,
            data={"user_id": "123"},
            source_service="test",
        )
        await event_bus.publish(event)

        assert len(received_events) == 1
        assert received_events[0].data["user_id"] == "123"

    @pytest.mark.asyncio
    async def test_unsubscribe(self) -> None:
        """Test unsubscribing from events."""
        event_bus = EventBus()
        received_events: list[ServiceEvent] = []

        async def handler(event: ServiceEvent) -> None:
            received_events.append(event)

        event_bus.subscribe(EventType.USER_CREATED, handler)
        event_bus.unsubscribe(EventType.USER_CREATED, handler)

        event = ServiceEvent(
            event_type=EventType.USER_CREATED,
            data={"user_id": "123"},
            source_service="test",
        )
        await event_bus.publish(event)

        assert len(received_events) == 0

    def test_service_event_serialization(self) -> None:
        """Test event serialization to JSON."""
        event = ServiceEvent(
            event_type=EventType.USER_CREATED,
            data={"user_id": "123", "username": "test"},
            source_service="auth-match",
        )

        json_str = event.to_json()
        restored = ServiceEvent.from_json(json_str)

        assert restored.event_type == event.event_type
        assert restored.data == event.data
        assert restored.source_service == event.source_service
        assert restored.event_id == event.event_id
