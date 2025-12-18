"""Wallet service for currency operations."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.gamification_billing.app.models.wallet import (
    Transaction,
    TransactionType,
    Wallet,
)
from shared.messaging.events import EventType, ServiceEvent, event_bus


class WalletService:
    """Service for wallet and transaction operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize wallet service."""
        self.db = db

    async def get_or_create_wallet(self, user_id: str) -> Wallet:
        """Get or create a wallet for a user."""
        result = await self.db.execute(select(Wallet).where(Wallet.user_id == user_id))
        wallet = result.scalar_one_or_none()

        if not wallet:
            wallet = Wallet(user_id=user_id)
            self.db.add(wallet)
            await self.db.flush()

        return wallet

    async def get_balance(self, user_id: str) -> float:
        """Get user's balance."""
        wallet = await self.get_or_create_wallet(user_id)
        return wallet.balance

    async def add_funds(
        self,
        user_id: str,
        amount: float,
        transaction_type: TransactionType,
        description: str,
        external_id: str | None = None,
        metadata: dict | None = None,
    ) -> Transaction:
        """Add funds to wallet."""
        wallet = await self.get_or_create_wallet(user_id)
        balance_before = wallet.balance
        wallet.balance += amount

        transaction = Transaction(
            wallet_id=wallet.id,
            transaction_type=transaction_type.value,
            amount=amount,
            balance_before=balance_before,
            balance_after=wallet.balance,
            description=description,
            external_id=external_id,
            metadata=metadata,
        )
        self.db.add(transaction)
        await self.db.flush()

        event = ServiceEvent(
            event_type=EventType.BALANCE_UPDATED,
            data={
                "user_id": user_id,
                "new_balance": wallet.balance,
                "amount": amount,
                "transaction_type": transaction_type.value,
            },
            source_service="gamification-billing",
        )
        await event_bus.publish(event)

        return transaction

    async def spend_funds(
        self,
        user_id: str,
        amount: float,
        description: str,
        metadata: dict | None = None,
    ) -> Transaction | None:
        """Spend funds from wallet. Returns None if insufficient funds."""
        wallet = await self.get_or_create_wallet(user_id)

        if wallet.balance < amount:
            return None

        balance_before = wallet.balance
        wallet.balance -= amount

        transaction = Transaction(
            wallet_id=wallet.id,
            transaction_type=TransactionType.SPEND.value,
            amount=-amount,
            balance_before=balance_before,
            balance_after=wallet.balance,
            description=description,
            metadata=metadata,
        )
        self.db.add(transaction)
        await self.db.flush()

        event = ServiceEvent(
            event_type=EventType.BALANCE_UPDATED,
            data={
                "user_id": user_id,
                "new_balance": wallet.balance,
                "amount": -amount,
                "transaction_type": TransactionType.SPEND.value,
            },
            source_service="gamification-billing",
        )
        await event_bus.publish(event)

        return transaction

    async def get_transactions(
        self, user_id: str, limit: int = 50, offset: int = 0
    ) -> list[Transaction]:
        """Get transactions for a user."""
        wallet = await self.get_or_create_wallet(user_id)

        result = await self.db.execute(
            select(Transaction)
            .where(Transaction.wallet_id == wallet.id)
            .order_by(Transaction.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def check_balance(self, user_id: str, amount: float) -> bool:
        """Check if user has sufficient balance."""
        wallet = await self.get_or_create_wallet(user_id)
        return wallet.balance >= amount
