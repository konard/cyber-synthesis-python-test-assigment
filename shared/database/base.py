"""Base database configuration and utilities."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Global engine reference (initialized per service)
_engine: AsyncEngine | None = None
_async_session: async_sessionmaker[AsyncSession] | None = None


def init_database(database_url: str) -> None:
    """Initialize the database engine and session factory.

    Args:
        database_url: PostgreSQL connection URL
    """
    global _engine, _async_session  # noqa: PLW0603

    _engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )
    _async_session = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency.

    Yields:
        Database session
    """
    if _async_session is None:
        msg = "Database not initialized. Call init_database() first."
        raise RuntimeError(msg)

    async with _async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
