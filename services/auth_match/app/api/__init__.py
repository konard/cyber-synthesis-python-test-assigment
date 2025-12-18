"""API routes for Auth-Match service."""

from __future__ import annotations

from fastapi import APIRouter

from services.auth_match.app.api.auth import router as auth_router
from services.auth_match.app.api.users import router as users_router
from services.auth_match.app.api.profiles import router as profiles_router
from services.auth_match.app.api.matches import router as matches_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
router.include_router(matches_router, prefix="/matches", tags=["matches"])

__all__ = ["router"]
