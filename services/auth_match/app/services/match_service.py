"""Match service for handling invitations and matches."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_match.app.models.match import (
    Invitation,
    InvitationStatus,
    InvitationType,
    Match,
)
from services.auth_match.app.schemas.match import InvitationCreate
from shared.messaging.events import EventType, ServiceEvent, event_bus


class MatchService:
    """Service for matching and invitation operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize match service.

        Args:
            db: Database session
        """
        self.db = db

    async def create_invitation(
        self, sender_id: str, invitation_data: InvitationCreate
    ) -> Invitation:
        """Create a new invitation.

        Args:
            sender_id: ID of the user sending the invitation
            invitation_data: Invitation data

        Returns:
            Created invitation
        """
        # Check for existing pending invitation
        existing = await self.db.execute(
            select(Invitation).where(
                Invitation.sender_id == sender_id,
                Invitation.recipient_id == invitation_data.recipient_id,
                Invitation.invitation_type == invitation_data.invitation_type.value,
                Invitation.status == InvitationStatus.PENDING,
            )
        )
        if existing.scalar_one_or_none():
            msg = "Pending invitation already exists"
            raise ValueError(msg)

        invitation = Invitation(
            sender_id=sender_id,
            recipient_id=invitation_data.recipient_id,
            invitation_type=invitation_data.invitation_type.value,
            message=invitation_data.message,
            context_data=invitation_data.context_data,
            event_id=invitation_data.event_id,
        )
        self.db.add(invitation)
        await self.db.flush()

        # Publish event based on invitation type
        event = ServiceEvent(
            event_type=EventType.INVITATION_SENT,
            data={
                "invitation_id": invitation.id,
                "sender_id": sender_id,
                "recipient_id": invitation_data.recipient_id,
                "invitation_type": invitation_data.invitation_type.value,
                "event_id": invitation_data.event_id,
            },
            source_service="auth-match",
        )
        await event_bus.publish(event)

        return invitation

    async def respond_to_invitation(
        self, invitation_id: str, user_id: str, accept: bool
    ) -> Invitation | None:
        """Respond to an invitation.

        Args:
            invitation_id: Invitation ID
            user_id: ID of the user responding
            accept: Whether to accept the invitation

        Returns:
            Updated invitation if found, None otherwise
        """
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.id == invitation_id,
                Invitation.recipient_id == user_id,
                Invitation.status == InvitationStatus.PENDING,
            )
        )
        invitation = result.scalar_one_or_none()
        if not invitation:
            return None

        invitation.status = (
            InvitationStatus.ACCEPTED if accept else InvitationStatus.DECLINED
        )
        invitation.responded_at = datetime.now(timezone.utc)

        # If accepted and it's a LIKE invitation, check for mutual match
        if accept and invitation.invitation_type == InvitationType.LIKE.value:
            await self._check_and_create_match(invitation)

        return invitation

    async def _check_and_create_match(self, invitation: Invitation) -> Match | None:
        """Check for mutual invitation and create match if both users liked each other.

        Args:
            invitation: The accepted invitation

        Returns:
            Created match if mutual, None otherwise
        """
        # Check if the original sender also received a like from the recipient
        mutual = await self.db.execute(
            select(Invitation).where(
                Invitation.sender_id == invitation.recipient_id,
                Invitation.recipient_id == invitation.sender_id,
                Invitation.invitation_type == InvitationType.LIKE.value,
                Invitation.status == InvitationStatus.ACCEPTED,
            )
        )
        mutual_invitation = mutual.scalar_one_or_none()

        if mutual_invitation:
            # Create match
            match = Match(
                user1_id=invitation.sender_id,
                user2_id=invitation.recipient_id,
                original_invitation_id=invitation.id,
            )
            self.db.add(match)
            await self.db.flush()

            # Publish match event
            event = ServiceEvent(
                event_type=EventType.MATCH_CREATED,
                data={
                    "match_id": match.id,
                    "user1_id": match.user1_id,
                    "user2_id": match.user2_id,
                },
                source_service="auth-match",
            )
            await event_bus.publish(event)

            return match
        return None

    async def get_user_invitations(
        self, user_id: str, sent: bool = False
    ) -> list[Invitation]:
        """Get invitations for a user.

        Args:
            user_id: User ID
            sent: If True, get sent invitations; otherwise get received

        Returns:
            List of invitations
        """
        if sent:
            query = select(Invitation).where(Invitation.sender_id == user_id)
        else:
            query = select(Invitation).where(Invitation.recipient_id == user_id)

        result = await self.db.execute(query.order_by(Invitation.created_at.desc()))
        return list(result.scalars().all())

    async def get_user_matches(self, user_id: str) -> list[Match]:
        """Get matches for a user.

        Args:
            user_id: User ID

        Returns:
            List of matches
        """
        result = await self.db.execute(
            select(Match)
            .where(
                or_(Match.user1_id == user_id, Match.user2_id == user_id),
                Match.is_active.is_(True),
            )
            .order_by(Match.created_at.desc())
        )
        return list(result.scalars().all())

    async def unmatch(self, match_id: str, user_id: str) -> Match | None:
        """Unmatch from a user.

        Args:
            match_id: Match ID
            user_id: ID of the user requesting unmatch

        Returns:
            Updated match if found, None otherwise
        """
        result = await self.db.execute(
            select(Match).where(
                Match.id == match_id,
                or_(Match.user1_id == user_id, Match.user2_id == user_id),
                Match.is_active.is_(True),
            )
        )
        match = result.scalar_one_or_none()
        if not match:
            return None

        match.is_active = False
        match.unmatched_at = datetime.now(timezone.utc)

        return match
