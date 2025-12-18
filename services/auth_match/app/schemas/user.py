"""User schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user."""

    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    is_invisible: bool | None = None


class UserResponse(BaseModel):
    """Schema for user response."""

    id: str
    email: str
    username: str
    is_active: bool
    is_verified: bool
    is_invisible: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""

    sub: str
    username: str
    email: str
