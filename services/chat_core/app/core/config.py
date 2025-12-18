"""Configuration settings for Chat-Core service."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Chat-Core service settings."""

    # Service info
    service_name: str = "chat-core"
    api_prefix: str = "/api/v1"
    debug: bool = False

    # Database
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/chat_core"
    )

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"

    # WebSocket
    websocket_ping_interval: int = 30

    # External AI API for translation
    ai_api_url: str = ""
    ai_api_key: str = ""

    # WebRTC/Agora settings
    agora_app_id: str = ""
    agora_app_certificate: str = ""

    # CORS
    cors_origins: list[str] = ["*"]

    class Config:
        """Pydantic config."""

        env_prefix = "CHAT_CORE_"


settings = Settings()
