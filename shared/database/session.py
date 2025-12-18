"""Database session management."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class DatabaseSession:
    """Database session configuration."""

    host: str
    port: int
    database: str
    username: str
    password: str

    @property
    def url(self) -> str:
        """Get the database URL.

        Returns:
            PostgreSQL connection URL
        """
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


def get_database_url(service_name: str = "default") -> str:
    """Get database URL from environment variables.

    Args:
        service_name: Name of the service for database selection

    Returns:
        Database connection URL
    """
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    database = os.getenv("DB_NAME", service_name)
    username = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")

    session = DatabaseSession(
        host=host,
        port=port,
        database=database,
        username=username,
        password=password,
    )
    return session.url
