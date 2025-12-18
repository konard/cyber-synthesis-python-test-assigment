"""Gamification API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.gamification_billing.app.schemas.dice import DiceRollResponse
from services.gamification_billing.app.schemas.rating import (
    LeaderboardEntry,
    RatingResponse,
)
from services.gamification_billing.app.services.gamification_service import (
    GamificationService,
)
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.get("/rating", response_model=RatingResponse)
async def get_my_rating(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current user's rating."""
    service = GamificationService(db)
    return await service.get_or_create_rating(current_user["sub"])


@router.post("/dice", response_model=DiceRollResponse)
async def roll_dice(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Roll the dice game."""
    service = GamificationService(db)
    result = await service.roll_dice(current_user["sub"])
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds to play",
        )
    return result


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    scope: str = Query("global", pattern="^(global|country|region|city)$"),
    scope_value: str | None = None,
    limit: int = Query(100, ge=1, le=500),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get leaderboard."""
    service = GamificationService(db)
    return await service.get_leaderboard(scope, scope_value, limit)
