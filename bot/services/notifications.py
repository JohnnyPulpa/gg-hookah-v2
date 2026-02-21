"""Notification service — format and send Telegram messages for order events.

Called by the notification_server when admin triggers status changes.
"""

import logging
from aiogram import Bot
from bot import db
from bot.templates import t
from bot.keyboards.main import order_actions_keyboard

log = logging.getLogger("gg-hookah-bot.notifications")

# Map event name → template key
EVENT_TEMPLATE_MAP = {
    "ORDER_CONFIRMED": "order_confirmed",
    "ON_THE_WAY": "order_on_the_way",
    "DELIVERED": "order_delivered",
    "SESSION_STARTED": "session_started",
    "SESSION_ENDING_BEFORE_02": "session_ending_before_02",
    "SESSION_ENDING_AFTER_02": "session_ending_after_02",
    "SESSION_ENDING": None,  # resolved dynamically
    "PICKUP_REQUESTED": "pickup_requested",
    "ORDER_COMPLETED": "order_completed",
    "ORDER_CANCELED": "order_canceled",
    "REBOWL_IN_PROGRESS": "rebowl_on_the_way",
    "REBOWL_DONE": "rebowl_done",
    "FREE_EXTENSION": "free_extension_used",
}

# Map event → order status (for attaching action buttons)
EVENT_TO_STATUS = {
    "ORDER_CONFIRMED": "CONFIRMED",
    "ON_THE_WAY": "ON_THE_WAY",
    "SESSION_STARTED": "SESSION_ACTIVE",
    "SESSION_ENDING": "SESSION_ENDING",
    "SESSION_ENDING_BEFORE_02": "SESSION_ENDING",
    "SESSION_ENDING_AFTER_02": "SESSION_ENDING",
}


def _resolve_session_ending() -> str:
    """Check Tbilisi time to decide which session_ending template to use."""
    from datetime import datetime
    import pytz
    tz = pytz.timezone("Asia/Tbilisi")
    now_local = datetime.now(tz)
    if 2 <= now_local.hour < 18:
        return "session_ending_after_02"
    return "session_ending_before_02"


async def send_notification(bot: Bot, event: str, telegram_id: int, data: dict) -> None:
    """Format and send a notification message to a Telegram user.

    Args:
        bot: aiogram Bot instance
        event: event name (e.g. "ORDER_CONFIRMED")
        telegram_id: user's Telegram ID
        data: dict with template variables (order_id_short, eta_text, etc.)
    """
    try:
        # Resolve template key
        if event == "SESSION_ENDING":
            template_key = _resolve_session_ending()
        else:
            template_key = EVENT_TEMPLATE_MAP.get(event)

        if not template_key:
            log.warning("No template for event %s", event)
            return

        # Get user language
        lang = await db.get_user_language(telegram_id)

        # Format message
        text = t(template_key, lang, **data)

        # Attach action buttons if applicable
        status = EVENT_TO_STATUS.get(event)
        reply_markup = order_actions_keyboard(lang, status) if status else None

        # Send
        await bot.send_message(telegram_id, text, reply_markup=reply_markup)
        log.info("Notification sent: event=%s telegram_id=%s", event, telegram_id)

    except Exception:
        log.exception("Failed to send notification: event=%s telegram_id=%s", event, telegram_id)
