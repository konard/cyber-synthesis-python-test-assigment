"""Wallet schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WalletResponse(BaseModel):
    """Schema for wallet response."""

    id: str
    user_id: str
    balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TransactionResponse(BaseModel):
    """Schema for transaction response."""

    id: str
    wallet_id: str
    transaction_type: str
    amount: float
    balance_before: float
    balance_after: float
    description: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class PurchaseRequest(BaseModel):
    """Schema for purchasing currency."""

    package_id: str
    payment_method_id: str | None = None


class SpendRequest(BaseModel):
    """Schema for spending currency."""

    amount: float = Field(..., gt=0)
    description: str
    metadata: dict[str, Any] | None = None
