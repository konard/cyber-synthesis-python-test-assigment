"""Comment schemas for API requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    """Schema for creating a comment."""

    post_id: str
    content: str
    parent_id: str | None = None


class CommentResponse(BaseModel):
    """Schema for comment response."""

    id: str
    post_id: str
    author_id: str
    parent_id: str | None = None
    content: str
    likes_count: int = 0
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
