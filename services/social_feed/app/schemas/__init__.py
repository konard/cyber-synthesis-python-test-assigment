"""Pydantic schemas for Social-Feed service."""

from __future__ import annotations

from services.social_feed.app.schemas.post import PostCreate, PostResponse, PostUpdate
from services.social_feed.app.schemas.comment import CommentCreate, CommentResponse
from services.social_feed.app.schemas.story import StoryCreate, StoryResponse

__all__ = [
    "PostCreate",
    "PostResponse",
    "PostUpdate",
    "CommentCreate",
    "CommentResponse",
    "StoryCreate",
    "StoryResponse",
]
