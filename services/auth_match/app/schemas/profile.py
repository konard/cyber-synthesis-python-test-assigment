"""Profile schemas for API requests and responses."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    """Schema for creating user profile."""

    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    display_name: str | None = Field(None, max_length=100)
    bio: str | None = None
    avatar_url: str | None = None
    cover_photo_url: str | None = None
    date_of_birth: date | None = None
    gender: str | None = Field(None, max_length=20)
    city: str | None = Field(None, max_length=100)
    region: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)
    phone_number: str | None = Field(None, max_length=20)
    website: str | None = None
    interests: list[str] | None = None
    languages: list[str] | None = None
    skills: list[str] | None = None
    hobbies: list[str] | None = None
    favorite_places: list[str] | None = None
    height_cm: int | None = None
    search_radius_km: int | None = Field(50, ge=1, le=500)
    preferences: dict[str, Any] | None = None
    notification_settings: dict[str, Any] | None = None
    privacy_settings: dict[str, Any] | None = None


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""

    first_name: str | None = None
    last_name: str | None = None
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    cover_photo_url: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    phone_number: str | None = None
    website: str | None = None
    interests: list[str] | None = None
    languages: list[str] | None = None
    skills: list[str] | None = None
    hobbies: list[str] | None = None
    favorite_places: list[str] | None = None
    height_cm: int | None = None
    search_radius_km: int | None = None
    preferences: dict[str, Any] | None = None
    notification_settings: dict[str, Any] | None = None
    privacy_settings: dict[str, Any] | None = None
    last_known_latitude: float | None = None
    last_known_longitude: float | None = None


class ProfileResponse(BaseModel):
    """Schema for profile response."""

    id: str
    user_id: str
    first_name: str | None = None
    last_name: str | None = None
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    cover_photo_url: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    phone_number: str | None = None
    website: str | None = None
    interests: list[str] | None = None
    languages: list[str] | None = None
    skills: list[str] | None = None
    hobbies: list[str] | None = None
    favorite_places: list[str] | None = None
    height_cm: int | None = None
    search_radius_km: int | None = None
    preferences: dict[str, Any] | None = None
    notification_settings: dict[str, Any] | None = None
    privacy_settings: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
