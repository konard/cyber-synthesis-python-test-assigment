"""API routes for Gamification & Billing service."""

from __future__ import annotations

from fastapi import APIRouter

from services.gamification_billing.app.api.wallet import router as wallet_router
from services.gamification_billing.app.api.gamification import (
    router as gamification_router,
)

router = APIRouter()
router.include_router(wallet_router, prefix="/wallet", tags=["wallet"])
router.include_router(
    gamification_router, prefix="/gamification", tags=["gamification"]
)

__all__ = ["router"]
