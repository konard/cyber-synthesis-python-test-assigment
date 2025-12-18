"""API routes for Events service."""

from __future__ import annotations

from fastapi import APIRouter

from services.events.app.api.events import router as events_router
from services.events.app.api.tickets import router as tickets_router

router = APIRouter()
router.include_router(events_router, prefix="/events", tags=["events"])
router.include_router(tickets_router, prefix="/tickets", tags=["tickets"])

__all__ = ["router"]
