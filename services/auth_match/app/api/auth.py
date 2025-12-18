"""Authentication API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_match.app.schemas.user import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from services.auth_match.app.services.user_service import UserService
from shared.database import get_db

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user
    """
    service = UserService(db)
    try:
        user = await service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Login and get access token.

    Args:
        login_data: Login credentials
        db: Database session

    Returns:
        JWT access token
    """
    service = UserService(db)
    result = await service.authenticate_user(login_data.username, login_data.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user, token = result
    return Token(access_token=token)
