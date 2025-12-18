"""Tests for Social-Feed service."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.social_feed.main import app
from services.social_feed.app.models.post import PostType


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
        assert response.json()["service"] == "social-feed"


class TestPostTypes:
    """Tests for post types."""

    def test_post_types_exist(self) -> None:
        """Test that all 4 required post types exist."""
        assert PostType.STANDARD.value == "standard"
        assert PostType.PAID.value == "paid"
        assert PostType.EVENT.value == "event"
        assert PostType.MARKETPLACE.value == "marketplace"

    def test_post_type_count(self) -> None:
        """Test that there are exactly 4 post types (as per requirements)."""
        assert len(PostType) == 4
