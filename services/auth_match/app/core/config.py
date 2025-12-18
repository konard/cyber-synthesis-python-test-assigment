"""Configuration settings for Auth-Match service."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Auth-Match service settings."""

    # Service info
    service_name: str = "auth-match"
    api_prefix: str = "/api/v1"
    debug: bool = False

    # Database
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/auth_match"
    )

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["*"]

    class Config:
        """Pydantic config."""

        env_prefix = "AUTH_MATCH_"


settings = Settings()
