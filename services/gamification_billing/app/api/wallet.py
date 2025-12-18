"""Wallet API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from services.gamification_billing.app.schemas.wallet import (
    TransactionResponse,
    WalletResponse,
)
from services.gamification_billing.app.services.wallet_service import WalletService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.get("/", response_model=WalletResponse)
async def get_wallet(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's wallet."""
    service = WalletService(db)
    return await service.get_or_create_wallet(current_user["sub"])


@router.get("/balance")
async def get_balance(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's balance."""
    service = WalletService(db)
    balance = await service.get_balance(current_user["sub"])
    return {"balance": balance}


@router.get("/transactions", response_model=list[TransactionResponse])
async def get_transactions(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get transaction history."""
    service = WalletService(db)
    return await service.get_transactions(current_user["sub"], limit, offset)


@router.get("/check/{amount}")
async def check_balance(
    amount: float,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Check if user has sufficient balance."""
    service = WalletService(db)
    has_funds = await service.check_balance(current_user["sub"], amount)
    return {"has_sufficient_funds": has_funds, "required_amount": amount}
