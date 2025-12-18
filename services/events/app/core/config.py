"""Configuration settings for Events service."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Events service settings."""

    service_name: str = "events"
    api_prefix: str = "/api/v1"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/events"
    jwt_secret_key: str = "your-secret-key-change-in-production"
    min_rating_to_create_event: float = 0.0
    cors_origins: list[str] = ["*"]

    class Config:
        """Pydantic config."""

        env_prefix = "EVENTS_"


settings = Settings()
