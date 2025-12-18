"""API routes for Chat-Core service."""

from __future__ import annotations

from fastapi import APIRouter

from services.chat_core.app.api.chats import router as chats_router
from services.chat_core.app.api.messages import router as messages_router

router = APIRouter()
router.include_router(chats_router, prefix="/chats", tags=["chats"])
router.include_router(messages_router, prefix="/messages", tags=["messages"])

__all__ = ["router"]
