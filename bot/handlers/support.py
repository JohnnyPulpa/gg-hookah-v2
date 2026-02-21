"""Catch-all handler for support messages.

F2.3: Any text message that isn't a command or button press
is saved as a support message and forwarded to admin.

IMPORTANT: This router must be registered LAST in bot_main.py
so it only catches messages not handled by other routers.
"""

import logging
from aiogram import Router, F
from aiogram.types import Message

from bot.db import (
    get_active_order,
    get_user_language,
    get_user_name,
    save_support_message,
)
from bot.templates import t
from bot.config import ADMIN_IDS

router = Router()
log = logging.getLogger("gg-hookah-bot.support")

# Thread type labels for admin notification
THREAD_LABELS = {
    "session": {"ru": "Сессия", "en": "Session"},
    "order": {"ru": "Заказ", "en": "Order"},
    "general": {"ru": "Общий", "en": "General"},
}


def _determine_thread(order: dict | None) -> tuple[str, str | None]:
    """Determine thread_type and thread_id from active order."""
    if not order:
        return "general", None
    status = order["status"]
    order_id = str(order["id"])
    if status in ("SESSION_ACTIVE", "SESSION_ENDING"):
        return "session", order_id
    return "order", order_id


@router.message(F.text)
async def catch_all_support(message: Message) -> None:
    """Save any unhandled text message as a support message."""
    user = message.from_user
    if not user or not message.text:
        return

    lang = await get_user_language(user.id)
    order = await get_active_order(user.id)
    thread_type, thread_id = _determine_thread(order)

    # Save to DB
    await save_support_message(
        telegram_id=user.id,
        text=message.text,
        thread_type=thread_type,
        thread_id=thread_id,
    )

    # Reply to client
    await message.answer(t("support_received", lang))

    # Notify admins
    client_name = await get_user_name(user.id)
    thread_label = THREAD_LABELS.get(thread_type, {}).get("ru", thread_type)
    admin_text = t(
        "admin_support_message",
        "ru",
        client_name=client_name,
        thread_label=thread_label,
        text=message.text,
    )
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_text)
        except Exception:
            log.warning("Failed to notify admin %s about support message", admin_id)

    log.info(
        "Support message from %s (type=%s): %s",
        user.id, thread_type, message.text[:80],
    )
