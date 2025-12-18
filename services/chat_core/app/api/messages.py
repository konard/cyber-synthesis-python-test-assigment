"""Message API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.chat_core.app.schemas.message import (
    MessageCreate,
    MessageResponse,
    QuickActionMessage,
)
from services.chat_core.app.services.chat_service import ChatService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: MessageCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Send a message.

    Args:
        message_data: Message data
        current_user: Current user from token
        db: Database session

    Returns:
        Created message
    """
    service = ChatService(db)
    message = await service.send_message(current_user["sub"], message_data)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found or access denied",
        )
    return message


@router.post(
    "/quick-action", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
async def send_quick_action(
    action_data: QuickActionMessage,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Send a quick action message.

    Args:
        action_data: Quick action data
        current_user: Current user from token
        db: Database session

    Returns:
        Created message
    """
    service = ChatService(db)
    message = await service.send_quick_action(current_user["sub"], action_data)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found or access denied",
        )
    return message


@router.get("/chat/{chat_id}", response_model=list[MessageResponse])
async def get_messages(
    chat_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get messages for a chat.

    Args:
        chat_id: Chat ID
        limit: Maximum number of messages
        offset: Offset for pagination
        current_user: Current user from token
        db: Database session

    Returns:
        List of messages
    """
    service = ChatService(db)
    return await service.get_messages(chat_id, current_user["sub"], limit, offset)
