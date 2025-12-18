"""Tests for Events service."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.events.main import app
from services.events.app.models.ticket import TicketStatus


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
        assert response.json()["service"] == "events"


class TestTicketStatuses:
    """Tests for ticket status types."""

    def test_ticket_statuses_exist(self) -> None:
        """Test that all ticket statuses exist."""
        assert TicketStatus.ACTIVE.value == "active"
        assert TicketStatus.USED.value == "used"
        assert TicketStatus.GIFTED.value == "gifted"
        assert TicketStatus.CANCELLED.value == "cancelled"
        assert TicketStatus.EXPIRED.value == "expired"
