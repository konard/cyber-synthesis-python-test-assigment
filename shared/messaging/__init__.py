"""Messaging utilities for inter-service communication."""

from __future__ import annotations

from shared.messaging.events import EventBus, ServiceEvent

__all__ = ["EventBus", "ServiceEvent"]
