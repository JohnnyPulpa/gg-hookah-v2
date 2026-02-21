"""GG HOOKAH Telegram Bot — entry point.

Runs aiogram 3.x polling bot with handlers for:
- /start, /help, /language
- Persistent buttons (Open App, My Order, Support)

Started by systemd: gg-hookah-bot.service
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN
from bot.handlers.start import router as start_router
from bot.handlers.order_actions import router as order_actions_router
from bot.notification_server import start_notification_server
from bot.services.session_timer import session_timer_loop

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("gg-hookah-bot")


async def main() -> None:
    """Initialize bot and start polling."""
    if not BOT_TOKEN or BOT_TOKEN.startswith("{{"):
        log.error("BOT_TOKEN is not set! Check /etc/gg-hookah/.env")
        sys.exit(1)

    bot = Bot(
        token=BOT_TOKEN,
        parse_mode=ParseMode.HTML,
    )
    dp = Dispatcher()

    # Register routers
    dp.include_router(order_actions_router)  # callback queries first
    dp.include_router(start_router)

    # Set bot commands menu
    from aiogram.types import BotCommand
    await bot.set_my_commands([
        BotCommand(command="start", description="Start / Restart bot"),
        BotCommand(command="help", description="Help"),
        BotCommand(command="language", description="Switch RU/EN"),
        BotCommand(command="admin", description="Admin panel login"),
    ])

    # Start notification HTTP server (runs in background)
    await start_notification_server(bot)
    log.info("Notification server ready on :5003")

    # Start session timer cron (checks every 60s for expiring sessions)
    asyncio.create_task(session_timer_loop(bot))
    log.info("Session timer cron started")

    log.info("Bot starting polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())