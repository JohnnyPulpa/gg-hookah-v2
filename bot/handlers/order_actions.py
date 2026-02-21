"""Handlers for client order actions via inline buttons.

F2.1: Cancel order, Ready for Pickup.
Callback data format: "action:<action_name>" for initial actions,
"confirm_cancel_yes" / "confirm_cancel_no" for cancel confirmation.
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.db import (
    get_active_order,
    get_user_language,
    get_user_name,
    cancel_order,
    set_ready_for_pickup,
)
from bot.templates import t
from bot.keyboards.main import confirm_cancel_inline
from bot.config import ADMIN_IDS

router = Router()
log = logging.getLogger("gg-hookah-bot.order-actions")


async def _notify_admins(bot, template_key: str, lang: str = "ru", **kwargs) -> None:
    """Send notification to all admin users."""
    text = t(template_key, lang, **kwargs)
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception:
            log.warning("Failed to notify admin %s", admin_id)


# --- Cancel flow ---

@router.callback_query(F.data == "action:cancel")
async def on_cancel_order(callback: CallbackQuery) -> None:
    """Client taps Cancel — show confirmation."""
    if not callback.from_user or not callback.message:
        return

    lang = await get_user_language(callback.from_user.id)
    order = await get_active_order(callback.from_user.id)

    if not order:
        msg = "Нет активного заказа." if lang == "ru" else "No active order."
        await callback.answer(msg, show_alert=True)
        return

    if order["status"] not in ("NEW", "CONFIRMED", "ON_THE_WAY"):
        msg = ("Отмена недоступна на этом этапе." if lang == "ru"
               else "Cancellation is not available at this stage.")
        await callback.answer(msg, show_alert=True)
        return

    # Show confirmation
    confirm_text = ("Вы уверены, что хотите отменить заказ?" if lang == "ru"
                    else "Are you sure you want to cancel the order?")
    await callback.message.answer(
        confirm_text,
        reply_markup=confirm_cancel_inline(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "confirm_cancel_yes")
async def on_confirm_cancel_yes(callback: CallbackQuery) -> None:
    """Client confirms cancel."""
    if not callback.from_user or not callback.message:
        return

    lang = await get_user_language(callback.from_user.id)
    order = await get_active_order(callback.from_user.id)

    if not order:
        msg = "Нет активного заказа." if lang == "ru" else "No active order."
        await callback.answer(msg, show_alert=True)
        return

    order_id = str(order["id"])
    order_id_short = order_id[:8]

    success = await cancel_order(order_id, callback.from_user.id)

    if success:
        # Confirm to client
        await callback.message.edit_text(t("order_canceled", lang, order_id_short=order_id_short))

        # Notify admins
        client_name = await get_user_name(callback.from_user.id)
        await _notify_admins(
            callback.bot,
            "admin_client_cancel",
            order_id_short=order_id_short,
            client_name=client_name,
        )
        log.info("Order %s canceled by client %s", order_id_short, callback.from_user.id)
    else:
        msg = ("Отмена недоступна на этом этапе." if lang == "ru"
               else "Cancellation is not available at this stage.")
        await callback.message.edit_text(msg)

    await callback.answer()


@router.callback_query(F.data == "confirm_cancel_no")
async def on_confirm_cancel_no(callback: CallbackQuery) -> None:
    """Client declines cancel."""
    if not callback.from_user or not callback.message:
        return

    lang = await get_user_language(callback.from_user.id)
    msg = "Отмена отклонена." if lang == "ru" else "Cancel declined."
    await callback.message.edit_text(msg)
    await callback.answer()


# --- Ready for Pickup ---

@router.callback_query(F.data == "action:ready_pickup")
async def on_ready_for_pickup(callback: CallbackQuery) -> None:
    """Client signals ready for hookah pickup."""
    if not callback.from_user or not callback.message:
        return

    lang = await get_user_language(callback.from_user.id)
    order = await get_active_order(callback.from_user.id)

    if not order:
        msg = "Нет активного заказа." if lang == "ru" else "No active order."
        await callback.answer(msg, show_alert=True)
        return

    if order["status"] not in ("SESSION_ACTIVE", "SESSION_ENDING"):
        msg = ("Эта функция доступна только во время сессии." if lang == "ru"
               else "This action is only available during an active session.")
        await callback.answer(msg, show_alert=True)
        return

    order_id = str(order["id"])
    order_id_short = order_id[:8]

    success = await set_ready_for_pickup(order_id, callback.from_user.id)

    if success:
        # Confirm to client
        await callback.message.edit_text(t("pickup_requested", lang))

        # Notify admins
        client_name = await get_user_name(callback.from_user.id)
        await _notify_admins(
            callback.bot,
            "admin_client_ready_pickup",
            order_id_short=order_id_short,
            client_name=client_name,
        )
        log.info("Ready for pickup: order %s, client %s", order_id_short, callback.from_user.id)
    else:
        msg = ("Не удалось обновить статус." if lang == "ru"
               else "Could not update order status.")
        await callback.answer(msg, show_alert=True)

    await callback.answer()
