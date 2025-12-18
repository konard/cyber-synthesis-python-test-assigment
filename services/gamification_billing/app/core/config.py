"""Configuration settings for Gamification & Billing service."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Gamification & Billing service settings."""

    service_name: str = "gamification-billing"
    api_prefix: str = "/api/v1"
    debug: bool = False
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/gamification"
    )
    jwt_secret_key: str = "your-secret-key-change-in-production"

    # Payment gateway
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    # SMS/Telegram for SOS
    telegram_bot_token: str = ""
    sms_api_url: str = ""
    sms_api_key: str = ""

    # Currency
    currency_name: str = "SuperSignal"
    dice_cost: float = 10.0

    cors_origins: list[str] = ["*"]

    class Config:
        """Pydantic config."""

        env_prefix = "GAMIFICATION_"


settings = Settings()
