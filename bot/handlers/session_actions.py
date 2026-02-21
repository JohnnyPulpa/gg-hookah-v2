"""Handlers for client session actions via inline buttons.

F2.2: Free +1h extension, Rebowl request.
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.db import (
    get_active_order,
    get_user_language,
    get_user_name,
    apply_free_extension,
    create_rebowl_request,
    has_active_rebowl,
    is_after_hours,
)
from bot.templates import t
from bot.config import ADMIN_IDS

router = Router()
log = logging.getLogger("gg-hookah-bot.session-actions")


async def _notify_admins(bot, template_key: str, **kwargs) -> None:
    """Send notification to all admin users."""
    text = t(template_key, "ru", **kwargs)
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception:
            log.warning("Failed to notify admin %s", admin_id)


# --- Free +1h Extension ---

@router.callback_query(F.data == "action:free_extend")
async def on_free_extend(callback: CallbackQuery) -> None:
    """Client taps Free +1h — extend session by 1 hour."""
    if not callback.from_user or not callback.message:
        return

    lang = await get_user_language(callback.from_user.id)
    order = await get_active_order(callback.from_user.id)

    if not order:
        msg = "Нет активного заказа." if lang == "ru" else "No active order."
        await callback.answer(msg, show_alert=True)
        return

    if order["status"] != "SESSION_ENDING":
        msg = ("Продление доступно только при статусе 'Сессия заканчивается'."
               if lang == "ru"
               else "Extension is only available when session is ending.")
        await callback.answer(msg, show_alert=True)
        return

    if order.get("free_extension_used"):
        msg = ("Бесплатное продление уже использовано."
               if lang == "ru"
               else "Free extension already used.")
        await callback.answer(msg, show_alert=True)
        return

    if is_after_hours():
        msg = ("Продление недоступно после 02:00."
               if lang == "ru"
               else "Extension unavailable after 02:00.")
        await callback.answer(msg, show_alert=True)
        return

    order_id = str(order["id"])
    order_id_short = order_id[:8]

    success = await apply_free_extension(order_id, callback.from_user.id)

    if success:
        await callback.message.edit_text(t("free_extension_used", lang))

        client_name = await get_user_name(callback.from_user.id)
        await _notify_admins(
            callback.bot,
            "admin_client_free_extend",
            order_id_short=order_id_short,
            client_name=client_name,
        )
        log.info("Free extension used: order %s, client %s", order_id_short, callback.from_user.id)
    else:
        msg = ("Не удалось продлить сессию." if lang == "ru"
               else "Could not extend session.")
        await callback.answer(msg, show_alert=True)

    await callback.answer()


# --- Rebowl Request ---

@router.callback_query(F.data == "action:rebowl")
async def on_rebowl_request(callback: CallbackQuery) -> None:
    """Client requests a new bowl (rebowl)."""
    if not callback.from_user or not callback.message:
        return

    lang = await get_user_language(callback.from_user.id)
    order = await get_active_order(callback.from_user.id)

    if not order:
        msg = "Нет активного заказа." if lang == "ru" else "No active order."
        await callback.answer(msg, show_alert=True)
        return

    if order["status"] not in ("SESSION_ACTIVE", "SESSION_ENDING"):
        msg = ("Новая чаша доступна только во время сессии."
               if lang == "ru"
               else "New bowl is only available during a session.")
        await callback.answer(msg, show_alert=True)
        return

    if is_after_hours():
        msg = ("Новая чаша недоступна после 02:00."
               if lang == "ru"
               else "New bowl unavailable after 02:00.")
        await callback.answer(msg, show_alert=True)
        return

    order_id = str(order["id"])

    if await has_active_rebowl(order_id):
        msg = ("Запрос на новую чашу уже отправлен."
               if lang == "ru"
               else "Bowl request already submitted.")
        await callback.answer(msg, show_alert=True)
        return

    mix_id = str(order["mix_id"]) if order.get("mix_id") else None
    if not mix_id:
        msg = ("Ошибка: микс не найден." if lang == "ru" else "Error: mix not found.")
        await callback.answer(msg, show_alert=True)
        return

    order_id_short = order_id[:8]

    success = await create_rebowl_request(order_id, callback.from_user.id, mix_id)

    if success:
        await callback.message.edit_text(t("rebowl_requested", lang))

        client_name = await get_user_name(callback.from_user.id)
        await _notify_admins(
            callback.bot,
            "admin_client_rebowl",
            order_id_short=order_id_short,
            client_name=client_name,
        )
        log.info("Rebowl requested: order %s, client %s", order_id_short, callback.from_user.id)
    else:
        msg = ("Не удалось создать запрос." if lang == "ru"
               else "Could not create request.")
        await callback.answer(msg, show_alert=True)

    await callback.answer()
