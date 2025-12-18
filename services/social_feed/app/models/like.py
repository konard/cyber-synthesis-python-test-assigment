"""Like model for posts and comments."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class Like(Base):
    """Like model for posts and comments."""

    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "target_id", "target_type", name="uq_like"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    target_id: Mapped[str] = mapped_column(String(36), index=True)
    target_type: Mapped[str] = mapped_column(String(10))  # 'post' or 'comment'

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        """String representation of Like."""
        return f"<Like(user={self.user_id}, target={self.target_id})>"
