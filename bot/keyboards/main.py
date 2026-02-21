"""Main keyboard layouts for the bot.

Spec 5.5: Persistent buttons — Open Mini App, Support, My Order.
Note: WebApp button requires HTTPS. Until SSL is ready, we use a regular
button and send the link as text.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

# --- Button labels RU/EN ---
LABELS = {
    "open_app": {"ru": "🏠 Открыть приложение", "en": "🏠 Open App"},
    "my_order": {"ru": "📋 Мой заказ", "en": "📋 My Order"},
    "support":  {"ru": "💬 Поддержка", "en": "💬 Support"},
    "language": {"ru": "🌐 English", "en": "🌐 Русский"},
}


def main_keyboard(lang: str = "ru", mini_app_url: str | None = None) -> ReplyKeyboardMarkup:
    """Persistent reply keyboard with main actions.

    If mini_app_url is provided and starts with https, uses WebApp button.
    Otherwise uses a regular button (handler sends link as text).
    """
    # Row 1: Open Mini App
    if mini_app_url and mini_app_url.startswith("https://"):
        app_btn = KeyboardButton(
            text=LABELS["open_app"][lang],
            web_app=WebAppInfo(url=mini_app_url),
        )
    else:
        app_btn = KeyboardButton(text=LABELS["open_app"][lang])

    # Row 2: My Order + Support
    order_btn = KeyboardButton(text=LABELS["my_order"][lang])
    support_btn = KeyboardButton(text=LABELS["support"][lang])

    return ReplyKeyboardMarkup(
        keyboard=[
            [app_btn],
            [order_btn, support_btn],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def order_actions_keyboard(
    lang: str = "ru",
    status: str = "",
    free_extension_used: bool = True,
    has_active_rebowl: bool = False,
    after_hours: bool = False,
) -> InlineKeyboardMarkup | None:
    """Inline action buttons based on current order status.

    Args:
        lang: user language
        status: current order status
        free_extension_used: whether free +1h was already used
        has_active_rebowl: whether there's an active rebowl request
        after_hours: whether it's after 02:00 Tbilisi time

    Returns None if no actions are available for the given status.
    """
    buttons = []

    # Cancel available before delivery
    if status in ("NEW", "CONFIRMED", "ON_THE_WAY"):
        cancel_text = "❌ Отменить заказ" if lang == "ru" else "❌ Cancel order"
        buttons.append([InlineKeyboardButton(
            text=cancel_text,
            callback_data="action:cancel",
        )])

    # Session ending actions (before 02:00 only)
    if status == "SESSION_ENDING" and not after_hours:
        # Free extension (once per session)
        if not free_extension_used:
            ext_text = "⏰ +1 час бесплатно" if lang == "ru" else "⏰ +1 hour free"
            buttons.append([InlineKeyboardButton(
                text=ext_text,
                callback_data="action:free_extend",
            )])

        # Rebowl (if no active request)
        if not has_active_rebowl:
            rebowl_text = "🔄 Новая чаша 50₾" if lang == "ru" else "🔄 New bowl 50₾"
            buttons.append([InlineKeyboardButton(
                text=rebowl_text,
                callback_data="action:rebowl",
            )])

    # Ready for pickup during session
    if status in ("SESSION_ACTIVE", "SESSION_ENDING"):
        pickup_text = "📦 Готов отдать кальян" if lang == "ru" else "📦 Ready for pickup"
        buttons.append([InlineKeyboardButton(
            text=pickup_text,
            callback_data="action:ready_pickup",
        )])

    return InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None


def order_created_inline(lang: str = "ru") -> InlineKeyboardMarkup:
    """Inline buttons after order is created: Support."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=LABELS["support"][lang],
            callback_data="support",
        )],
    ])


def confirm_cancel_inline(lang: str = "ru") -> InlineKeyboardMarkup:
    """Confirmation for cancel order."""
    yes = "Да, отменить" if lang == "ru" else "Yes, cancel"
    no = "Нет" if lang == "ru" else "No"
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"✅ {yes}", callback_data="confirm_cancel_yes"),
            InlineKeyboardButton(text=f"❌ {no}", callback_data="confirm_cancel_no"),
        ],
    ])