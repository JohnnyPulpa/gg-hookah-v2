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


def order_actions_keyboard(lang: str = "ru", status: str = "") -> InlineKeyboardMarkup | None:
    """Inline action buttons based on current order status.

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