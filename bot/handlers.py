from __future__ import annotations

from typing import Any

from core.config import Settings


def create_bot(settings: Settings) -> tuple[Any, Any]:
    try:
        from aiogram import Bot, Dispatcher
    except ImportError as exc:
        raise RuntimeError("Aiogram is required to run the bot.") from exc

    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is required to start the bot.")

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    return bot, dp
