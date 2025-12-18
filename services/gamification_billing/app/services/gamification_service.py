"""Gamification service for ratings and dice game."""

from __future__ import annotations

import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.gamification_billing.app.core.config import settings
from services.gamification_billing.app.models.rating import UserRating
from services.gamification_billing.app.models.wallet import TransactionType
from services.gamification_billing.app.schemas.dice import DiceRollResponse
from services.gamification_billing.app.schemas.rating import LeaderboardEntry
from services.gamification_billing.app.services.wallet_service import WalletService
from shared.messaging.events import EventType, ServiceEvent, event_bus


# Dice rewards configuration
DICE_REWARDS = [
    {"roll": 1, "type": "currency", "min": 5, "max": 10, "desc": "Small reward"},
    {"roll": 2, "type": "currency", "min": 10, "max": 20, "desc": "Medium reward"},
    {"roll": 3, "type": "currency", "min": 15, "max": 30, "desc": "Nice reward"},
    {"roll": 4, "type": "currency", "min": 20, "max": 40, "desc": "Great reward"},
    {"roll": 5, "type": "currency", "min": 30, "max": 50, "desc": "Excellent reward"},
    {"roll": 6, "type": "currency", "min": 50, "max": 100, "desc": "Jackpot!"},
]


class GamificationService:
    """Service for gamification features."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize gamification service."""
        self.db = db
        self.wallet_service = WalletService(db)

    async def get_or_create_rating(self, user_id: str) -> UserRating:
        """Get or create rating for user."""
        result = await self.db.execute(
            select(UserRating).where(UserRating.user_id == user_id)
        )
        rating = result.scalar_one_or_none()

        if not rating:
            rating = UserRating(user_id=user_id)
            self.db.add(rating)
            await self.db.flush()

        return rating

    async def update_rating(
        self,
        user_id: str,
        posts_delta: int = 0,
        comments_delta: int = 0,
        likes_delta: int = 0,
        events_created_delta: int = 0,
        events_attended_delta: int = 0,
        matches_delta: int = 0,
    ) -> UserRating:
        """Update user rating based on activity."""
        rating = await self.get_or_create_rating(user_id)

        rating.posts_count += posts_delta
        rating.comments_count += comments_delta
        rating.likes_received += likes_delta
        rating.events_created += events_created_delta
        rating.events_attended += events_attended_delta
        rating.matches_count += matches_delta

        # Calculate score (simple formula)
        rating.score = (
            rating.posts_count * 10
            + rating.comments_count * 2
            + rating.likes_received * 1
            + rating.events_created * 20
            + rating.events_attended * 5
            + rating.matches_count * 15
        )

        # Calculate level
        rating.level = int(rating.score / 100) + 1

        event = ServiceEvent(
            event_type=EventType.RATING_CHANGED,
            data={
                "user_id": user_id,
                "new_score": rating.score,
                "new_level": rating.level,
            },
            source_service="gamification-billing",
        )
        await event_bus.publish(event)

        return rating

    async def roll_dice(self, user_id: str) -> DiceRollResponse | None:
        """Roll the dice game.

        Returns None if user has insufficient funds.
        """
        # Check and spend dice cost
        transaction = await self.wallet_service.spend_funds(
            user_id,
            settings.dice_cost,
            f"Dice game roll (cost: {settings.dice_cost} {settings.currency_name})",
        )
        if not transaction:
            return None

        # Roll the dice
        roll_value = random.randint(1, 6)
        reward_config = DICE_REWARDS[roll_value - 1]

        # Calculate reward
        reward_value = random.randint(reward_config["min"], reward_config["max"])

        # Award the reward
        await self.wallet_service.add_funds(
            user_id,
            float(reward_value),
            TransactionType.REWARD,
            f"Dice game reward (rolled {roll_value}): {reward_config['desc']}",
            metadata={"roll": roll_value, "reward_type": reward_config["type"]},
        )

        wallet = await self.wallet_service.get_or_create_wallet(user_id)

        event = ServiceEvent(
            event_type=EventType.REWARD_EARNED,
            data={
                "user_id": user_id,
                "roll_value": roll_value,
                "reward_value": reward_value,
            },
            source_service="gamification-billing",
        )
        await event_bus.publish(event)

        return DiceRollResponse(
            roll_value=roll_value,
            reward_type=reward_config["type"],
            reward_value=reward_value,
            reward_description=reward_config["desc"],
            new_balance=wallet.balance,
        )

    async def get_leaderboard(
        self,
        scope: str = "global",
        scope_value: str | None = None,
        limit: int = 100,
    ) -> list[LeaderboardEntry]:
        """Get leaderboard by scope."""
        query = select(UserRating)

        if scope == "country" and scope_value:
            query = query.where(UserRating.country == scope_value)
        elif scope == "region" and scope_value:
            query = query.where(UserRating.region == scope_value)
        elif scope == "city" and scope_value:
            query = query.where(UserRating.city == scope_value)

        query = query.order_by(UserRating.score.desc()).limit(limit)

        result = await self.db.execute(query)
        ratings = list(result.scalars().all())

        return [
            LeaderboardEntry(
                rank=i + 1,
                user_id=r.user_id,
                score=r.score,
                level=r.level,
            )
            for i, r in enumerate(ratings)
        ]
