"""Wallet and transaction models for virtual currency."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class TransactionType(str, Enum):
    """Types of transactions."""

    PURCHASE = "purchase"  # Real money -> currency
    SPEND = "spend"  # Currency spent on feature
    EARN = "earn"  # Currency earned from activity
    REWARD = "reward"  # Currency from dice game
    TRANSFER = "transfer"  # User to user transfer
    REFUND = "refund"  # Refund


class Wallet(Base):
    """User wallet for virtual currency (SuperSignal)."""

    __tablename__ = "wallets"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        """String representation of Wallet."""
        return f"<Wallet(user={self.user_id}, balance={self.balance})>"


class Transaction(Base):
    """Transaction record for currency movements."""

    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    wallet_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("wallets.id"), index=True
    )
    transaction_type: Mapped[str] = mapped_column(String(20))
    amount: Mapped[float] = mapped_column(Float)
    balance_before: Mapped[float] = mapped_column(Float)
    balance_after: Mapped[float] = mapped_column(Float)

    # Description and metadata
    description: Mapped[str | None] = mapped_column(Text)
    metadata: Mapped[dict | None] = mapped_column(JSONB)

    # External reference (payment gateway, etc.)
    external_id: Mapped[str | None] = mapped_column(String(100))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        """String representation of Transaction."""
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"
