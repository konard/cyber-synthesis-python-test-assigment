"""Pydantic schemas for Chat-Core service."""

from __future__ import annotations

from services.chat_core.app.schemas.chat import ChatCreate, ChatResponse
from services.chat_core.app.schemas.message import (
    MessageCreate,
    MessageResponse,
    QuickActionMessage,
)

__all__ = [
    "ChatCreate",
    "ChatResponse",
    "MessageCreate",
    "MessageResponse",
    "QuickActionMessage",
]
