"""API routes for Social-Feed service."""

from __future__ import annotations

from fastapi import APIRouter

from services.social_feed.app.api.posts import router as posts_router
from services.social_feed.app.api.stories import router as stories_router

router = APIRouter()
router.include_router(posts_router, prefix="/posts", tags=["posts"])
router.include_router(stories_router, prefix="/stories", tags=["stories"])

__all__ = ["router"]
