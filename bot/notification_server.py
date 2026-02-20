"""HTTP notification server — receives events from admin panel.

Runs on 127.0.0.1:5003 as aiohttp web app alongside the bot polling loop.
Admin sends POST /notify with JSON payload to trigger Telegram notifications.
"""

import logging
from aiohttp import web
from aiogram import Bot
from bot.services.notifications import send_notification

log = logging.getLogger("gg-hookah-bot.notify-server")

REQUIRED_FIELDS = ("event", "telegram_id", "order_id_short")


async def handle_notify(request: web.Request) -> web.Response:
    """POST /notify — send a notification to a user."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "Invalid JSON"}, status=400)

    # Validate required fields
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return web.json_response(
            {"ok": False, "error": f"Missing fields: {', '.join(missing)}"},
            status=400,
        )

    event = data.pop("event")
    telegram_id = data.pop("telegram_id")

    # Everything else in data becomes template variables
    bot: Bot = request.app["bot"]
    await send_notification(bot, event, telegram_id, data)

    return web.json_response({"ok": True})


async def handle_health(request: web.Request) -> web.Response:
    """GET /health — simple health check."""
    return web.json_response({"status": "ok"})


def create_app(bot: Bot) -> web.Application:
    """Create aiohttp app with bot instance attached."""
    app = web.Application()
    app["bot"] = bot
    app.router.add_post("/notify", handle_notify)
    app.router.add_get("/health", handle_health)
    return app


async def start_notification_server(bot: Bot) -> None:
    """Start the notification HTTP server (non-blocking)."""
    app = create_app(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 5003)
    await site.start()
    log.info("Notification server started on http://127.0.0.1:5003")
