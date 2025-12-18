"""Configuration settings for Geo service."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Geo service settings."""

    service_name: str = "geo"
    api_prefix: str = "/api/v1"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/geo"
    jwt_secret_key: str = "your-secret-key-change-in-production"
    external_places_api_url: str = ""
    external_places_api_key: str = ""
    cache_ttl_seconds: int = 900
    cors_origins: list[str] = ["*"]

    class Config:
        """Pydantic config."""

        env_prefix = "GEO_"


settings = Settings()
