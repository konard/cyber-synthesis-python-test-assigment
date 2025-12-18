"""Pydantic schemas for Auth-Match service."""

from __future__ import annotations

from services.auth_match.app.schemas.user import (
    Token,
    TokenData,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from services.auth_match.app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from services.auth_match.app.schemas.match import (
    InvitationCreate,
    InvitationResponse,
    MatchResponse,
)

__all__ = [
    "Token",
    "TokenData",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "ProfileCreate",
    "ProfileResponse",
    "ProfileUpdate",
    "InvitationCreate",
    "InvitationResponse",
    "MatchResponse",
]
