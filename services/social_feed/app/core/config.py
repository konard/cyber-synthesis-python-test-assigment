"""Configuration settings for Social-Feed service."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Social-Feed service settings."""

    service_name: str = "social-feed"
    api_prefix: str = "/api/v1"
    debug: bool = False
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/social_feed"
    )
    jwt_secret_key: str = "your-secret-key-change-in-production"
    story_expiration_hours: int = 24
    cors_origins: list[str] = ["*"]

    class Config:
        """Pydantic config."""

        env_prefix = "SOCIAL_FEED_"


settings = Settings()
