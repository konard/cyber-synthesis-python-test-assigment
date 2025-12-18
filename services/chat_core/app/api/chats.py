"""Chat API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.chat_core.app.schemas.chat import ChatCreate, ChatResponse
from services.chat_core.app.services.chat_service import ChatService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new chat.

    Args:
        chat_data: Chat creation data
        current_user: Current user from token
        db: Database session

    Returns:
        Created chat
    """
    service = ChatService(db)
    chat = await service.create_chat(current_user["sub"], chat_data)
    return chat


@router.get("/", response_model=list[ChatResponse])
async def get_chats(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get all chats for current user.

    Args:
        current_user: Current user from token
        db: Database session

    Returns:
        List of chats
    """
    service = ChatService(db)
    return await service.get_user_chats(current_user["sub"])


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get chat by ID.

    Args:
        chat_id: Chat ID
        current_user: Current user from token
        db: Database session

    Returns:
        Chat
    """
    service = ChatService(db)
    chat = await service.get_chat(chat_id, current_user["sub"])
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    return chat


@router.post("/{chat_id}/read")
async def mark_as_read(
    chat_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Mark all messages in chat as read.

    Args:
        chat_id: Chat ID
        current_user: Current user from token
        db: Database session

    Returns:
        Number of messages marked as read
    """
    service = ChatService(db)
    count = await service.mark_as_read(chat_id, current_user["sub"])
    return {"marked_as_read": count}
