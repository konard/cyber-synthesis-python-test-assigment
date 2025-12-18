"""Tests for Auth-Match service."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.auth_match.main import app
from services.auth_match.app.models.match import InvitationType


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
        assert response.json()["service"] == "auth-match"


class TestInvitationTypes:
    """Tests for invitation type enum."""

    def test_invitation_types_exist(self) -> None:
        """Test that all required invitation types exist."""
        assert InvitationType.LIKE.value == "like"
        assert InvitationType.EVENT_INVITE.value == "event_invite"
        assert InvitationType.CHAT_REQUEST.value == "chat_request"
        assert InvitationType.ACTIVITY_PROPOSAL.value == "activity_proposal"

    def test_invitation_type_count(self) -> None:
        """Test that there are exactly 4 invitation types (as per requirements)."""
        assert len(InvitationType) == 4
