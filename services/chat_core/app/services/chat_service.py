"""Chat service for messaging operations."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.chat_core.app.models.chat import Chat
from services.chat_core.app.models.message import Message, MessageType, QuickAction
from services.chat_core.app.schemas.chat import ChatCreate
from services.chat_core.app.schemas.message import MessageCreate, QuickActionMessage
from shared.messaging.events import EventType, ServiceEvent, event_bus


class ChatService:
    """Service for chat and messaging operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize chat service.

        Args:
            db: Database session
        """
        self.db = db

    async def create_chat(self, user_id: str, chat_data: ChatCreate) -> Chat:
        """Create a new chat.

        Args:
            user_id: ID of the user creating the chat
            chat_data: Chat creation data

        Returns:
            Created chat
        """
        # Check if chat already exists between these users
        existing = await self.db.execute(
            select(Chat).where(
                or_(
                    (Chat.user1_id == user_id) & (Chat.user2_id == chat_data.user2_id),
                    (Chat.user1_id == chat_data.user2_id) & (Chat.user2_id == user_id),
                ),
                Chat.is_active.is_(True),
            )
        )
        if existing_chat := existing.scalar_one_or_none():
            return existing_chat

        chat = Chat(
            user1_id=user_id,
            user2_id=chat_data.user2_id,
            match_id=chat_data.match_id,
        )
        self.db.add(chat)
        await self.db.flush()

        # Publish event
        event = ServiceEvent(
            event_type=EventType.CHAT_CREATED,
            data={
                "chat_id": chat.id,
                "user1_id": user_id,
                "user2_id": chat_data.user2_id,
                "match_id": chat_data.match_id,
            },
            source_service="chat-core",
        )
        await event_bus.publish(event)

        return chat

    async def get_chat(self, chat_id: str, user_id: str) -> Chat | None:
        """Get a chat by ID.

        Args:
            chat_id: Chat ID
            user_id: User ID for authorization

        Returns:
            Chat if found and user is a participant, None otherwise
        """
        result = await self.db.execute(
            select(Chat).where(
                Chat.id == chat_id,
                or_(Chat.user1_id == user_id, Chat.user2_id == user_id),
            )
        )
        return result.scalar_one_or_none()

    async def get_user_chats(self, user_id: str) -> list[Chat]:
        """Get all chats for a user.

        Args:
            user_id: User ID

        Returns:
            List of chats
        """
        result = await self.db.execute(
            select(Chat)
            .where(
                or_(Chat.user1_id == user_id, Chat.user2_id == user_id),
                Chat.is_active.is_(True),
            )
            .order_by(Chat.last_message_at.desc().nullsfirst())
        )
        return list(result.scalars().all())

    async def send_message(
        self, user_id: str, message_data: MessageCreate
    ) -> Message | None:
        """Send a message.

        Args:
            user_id: ID of the sender
            message_data: Message data

        Returns:
            Created message if successful, None if chat not found
        """
        # Verify chat exists and user is a participant
        chat = await self.get_chat(message_data.chat_id, user_id)
        if not chat:
            return None

        message = Message(
            chat_id=message_data.chat_id,
            sender_id=user_id,
            message_type=message_data.message_type.value,
            content=message_data.content,
            media_url=message_data.media_url,
            media_thumbnail_url=message_data.media_thumbnail_url,
            media_metadata=message_data.media_metadata,
            structured_data=message_data.structured_data,
        )
        self.db.add(message)

        # Update chat's last message timestamp
        chat.last_message_at = datetime.now(timezone.utc)

        await self.db.flush()

        # Publish event
        event = ServiceEvent(
            event_type=EventType.MESSAGE_SENT,
            data={
                "message_id": message.id,
                "chat_id": chat.id,
                "sender_id": user_id,
                "message_type": message_data.message_type.value,
            },
            source_service="chat-core",
        )
        await event_bus.publish(event)

        return message

    async def send_quick_action(
        self, user_id: str, action_data: QuickActionMessage
    ) -> Message | None:
        """Send a quick action message.

        Args:
            user_id: ID of the sender
            action_data: Quick action data

        Returns:
            Created message if successful, None if chat not found
        """
        chat = await self.get_chat(action_data.chat_id, user_id)
        if not chat:
            return None

        message = Message(
            chat_id=action_data.chat_id,
            sender_id=user_id,
            message_type=MessageType.QUICK_ACTION.value,
            quick_action_type=action_data.action_type.value,
            structured_data=action_data.data,
        )
        self.db.add(message)

        chat.last_message_at = datetime.now(timezone.utc)
        await self.db.flush()

        # Trigger external service based on action type
        await self._handle_quick_action(action_data, message, user_id)

        return message

    async def _handle_quick_action(
        self, action_data: QuickActionMessage, message: Message, user_id: str
    ) -> None:
        """Handle quick action by calling external service.

        Args:
            action_data: Quick action data
            message: Created message
            user_id: User ID
        """
        # Publish event based on action type
        if action_data.action_type == QuickAction.CREATE_EVENT:
            event = ServiceEvent(
                event_type=EventType.EVENT_CREATED,
                data={
                    "source": "chat",
                    "message_id": message.id,
                    "user_id": user_id,
                    "event_data": action_data.data,
                },
                source_service="chat-core",
            )
            await event_bus.publish(event)

    async def get_messages(
        self, chat_id: str, user_id: str, limit: int = 50, offset: int = 0
    ) -> list[Message]:
        """Get messages for a chat.

        Args:
            chat_id: Chat ID
            user_id: User ID for authorization
            limit: Maximum number of messages
            offset: Offset for pagination

        Returns:
            List of messages
        """
        # Verify user is a participant
        chat = await self.get_chat(chat_id, user_id)
        if not chat:
            return []

        result = await self.db.execute(
            select(Message)
            .where(Message.chat_id == chat_id, Message.is_deleted.is_(False))
            .order_by(Message.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def mark_as_read(self, chat_id: str, user_id: str) -> int:
        """Mark all messages in chat as read.

        Args:
            chat_id: Chat ID
            user_id: User ID

        Returns:
            Number of messages marked as read
        """
        chat = await self.get_chat(chat_id, user_id)
        if not chat:
            return 0

        # Get the other user's ID
        other_user_id = chat.user2_id if chat.user1_id == user_id else chat.user1_id

        result = await self.db.execute(
            select(Message).where(
                Message.chat_id == chat_id,
                Message.sender_id == other_user_id,
                Message.is_read.is_(False),
            )
        )
        messages = list(result.scalars().all())

        now = datetime.now(timezone.utc)
        for message in messages:
            message.is_read = True
            message.read_at = now

        return len(messages)
