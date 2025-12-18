"""Tests for Gamification & Billing service."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.gamification_billing.main import app
from services.gamification_billing.app.models.wallet import TransactionType
from services.gamification_billing.app.models.subscription import SubscriptionTier


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
        assert response.json()["service"] == "gamification-billing"


class TestTransactionTypes:
    """Tests for transaction types."""

    def test_transaction_types_exist(self) -> None:
        """Test that all transaction types exist."""
        assert TransactionType.PURCHASE.value == "purchase"
        assert TransactionType.SPEND.value == "spend"
        assert TransactionType.EARN.value == "earn"
        assert TransactionType.REWARD.value == "reward"
        assert TransactionType.TRANSFER.value == "transfer"
        assert TransactionType.REFUND.value == "refund"


class TestSubscriptionTiers:
    """Tests for subscription tiers."""

    def test_subscription_tiers_exist(self) -> None:
        """Test that all subscription tiers exist."""
        assert SubscriptionTier.FREE.value == "free"
        assert SubscriptionTier.BASIC.value == "basic"
        assert SubscriptionTier.PREMIUM.value == "premium"
        assert SubscriptionTier.VIP.value == "vip"


class TestDiceGame:
    """Tests for dice game mechanics."""

    def test_dice_rewards_configuration(self) -> None:
        """Test that dice rewards are properly configured."""
        from services.gamification_billing.app.services.gamification_service import (
            DICE_REWARDS,
        )

        assert len(DICE_REWARDS) == 6  # One for each die face
        for i, reward in enumerate(DICE_REWARDS, 1):
            assert reward["roll"] == i
            assert "type" in reward
            assert "min" in reward
            assert "max" in reward
            assert reward["min"] <= reward["max"]
