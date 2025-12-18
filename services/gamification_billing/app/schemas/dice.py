"""Dice game schemas for API requests and responses."""

from __future__ import annotations


from pydantic import BaseModel


class DiceRollRequest(BaseModel):
    """Schema for rolling the dice."""

    pass  # Cost is fixed in settings


class DiceRollResponse(BaseModel):
    """Schema for dice roll result."""

    roll_value: int  # 1-6
    reward_type: str  # 'currency', 'status', 'boost', etc.
    reward_value: float | int | str
    reward_description: str
    new_balance: float


class RewardConfig(BaseModel):
    """Configuration for dice rewards."""

    roll_value: int
    reward_type: str
    min_value: float | int
    max_value: float | int
    probability_weight: float = 1.0
