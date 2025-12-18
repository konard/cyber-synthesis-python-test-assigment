"""Tests for Chat-Core service."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.chat_core.main import app
from services.chat_core.app.models.message import MessageType, QuickAction


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "chat-core"


class TestQuickActions:
    """Tests for quick action types."""

    def test_quick_action_types_exist(self) -> None:
        """Test that all required quick action types exist (4 buttons)."""
        assert QuickAction.PROPOSE_MEETING.value == "propose_meeting"
        assert QuickAction.SHARE_LOCATION.value == "share_location"
        assert QuickAction.CREATE_EVENT.value == "create_event"
        assert QuickAction.SEND_GIFT.value == "send_gift"

    def test_quick_action_count(self) -> None:
        """Test that there are exactly 4 quick actions (as per requirements)."""
        assert len(QuickAction) == 4


class TestMessageTypes:
    """Tests for message types."""

    def test_message_types_exist(self) -> None:
        """Test that all message types exist."""
        assert MessageType.TEXT.value == "text"
        assert MessageType.IMAGE.value == "image"
        assert MessageType.VIDEO.value == "video"
        assert MessageType.AUDIO.value == "audio"
        assert MessageType.FILE.value == "file"
        assert MessageType.LOCATION.value == "location"
        assert MessageType.QUICK_ACTION.value == "quick_action"
        assert MessageType.SYSTEM.value == "system"
