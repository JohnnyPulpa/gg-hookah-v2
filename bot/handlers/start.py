"""Handlers for /start, /help, and persistent button presses.

Spec 5.5: /start shows greeting + persistent keyboard.
Spec 5.3: Language from users.language.
"""

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.db import get_user_language, get_active_order, ensure_user_exists, has_active_rebowl, is_after_hours
from bot.templates import t
from bot.keyboards.main import main_keyboard, order_actions_keyboard, LABELS
from bot.config import MINI_APP_URL, DOMAIN

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start — greet user, create user record, show keyboard."""
    user = message.from_user
    if not user:
        return

    # Ensure user exists in DB
    await ensure_user_exists(
        telegram_id=user.id,
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        username=user.username or "",
    )

    lang = await get_user_language(user.id)
    await message.answer(
        t("welcome", lang),
        reply_markup=main_keyboard(lang, MINI_APP_URL),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help — show available actions."""
    user = message.from_user
    if not user:
        return
    lang = await get_user_language(user.id)
    await message.answer(t("help", lang))


@router.message(Command("language"))
async def cmd_language(message: Message) -> None:
    """Handle /language — toggle RU/EN."""
    user = message.from_user
    if not user:
        return

    # Get current language and toggle
    current = await get_user_language(user.id)
    new_lang = "en" if current == "ru" else "ru"

    # Update in DB
    from bot.db import execute
    await execute(
        "UPDATE users SET language = :lang, updated_at = now() WHERE telegram_id = :tid",
        {"lang": new_lang, "tid": user.id},
    )

    # Send confirmation with updated keyboard
    confirm = "Language switched to English" if new_lang == "en" else "Язык переключён на русский"
    await message.answer(
        confirm,
        reply_markup=main_keyboard(new_lang, MINI_APP_URL),
    )
@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    """Handle /admin — generate login link for admin panel."""
    user = message.from_user
    if not user:
        return

    # Check if user is admin
    from admin.auth import is_admin, generate_login_token
    if not is_admin(user.id):
        lang = await get_user_language(user.id)
        deny = "⛔ Доступ запрещён." if lang == "ru" else "⛔ Access denied."
        await message.answer(deny)
        return

    # Generate signed token and build URL
    token = generate_login_token(user.id)
    url = f"https://{DOMAIN}/admin/auth/login?token={token}"

    await message.answer(
        f"🔐 Admin Panel\n\n"
        f"Your login link (valid 5 min):\n{url}\n\n"
        f"Do not share this link.",
        disable_web_page_preview=True,
    )

@router.message(F.text.in_({
    LABELS["my_order"]["ru"],
    LABELS["my_order"]["en"],
}))
async def btn_my_order(message: Message) -> None:
    """Handle 'My Order' persistent button press."""
    user = message.from_user
    if not user:
        return

    lang = await get_user_language(user.id)
    order = await get_active_order(user.id)

    if not order:
        await message.answer(t("no_active_order", lang))
        return

    # Format order info
    status = order["status"]
    mix_name = order.get("mix_name", "—")
    order_id_short = str(order["id"])[:8]

    status_labels = {
        "NEW": {"ru": "🆕 Новый", "en": "🆕 New"},
        "CONFIRMED": {"ru": "✅ Подтверждён", "en": "✅ Confirmed"},
        "ON_THE_WAY": {"ru": "🚗 В пути", "en": "🚗 On the way"},
        "DELIVERED": {"ru": "📦 Доставлен", "en": "📦 Delivered"},
        "SESSION_ACTIVE": {"ru": "⏱ Сессия", "en": "⏱ Session active"},
        "SESSION_ENDING": {"ru": "⚠️ Сессия заканчивается", "en": "⚠️ Session ending"},
        "WAITING_FOR_PICKUP": {"ru": "📦 Ожидает забора", "en": "📦 Waiting for pickup"},
    }
    status_text = status_labels.get(status, {}).get(lang, status)

    if lang == "ru":
        text = (
            f"📋 Заказ #{order_id_short}\n\n"
            f"Статус: {status_text}\n"
            f"Микс: {mix_name}\n"
            f"Кальянов: {order.get('hookah_count', 1)}"
        )
    else:
        text = (
            f"📋 Order #{order_id_short}\n\n"
            f"Status: {status_text}\n"
            f"Mix: {mix_name}\n"
            f"Hookahs: {order.get('hookah_count', 1)}"
        )

    # Add session timer if active
    if order.get("session_ends_at") and status in ("SESSION_ACTIVE", "SESSION_ENDING"):
        from datetime import datetime, timezone
        ends = order["session_ends_at"]
        if ends.tzinfo is None:
            ends = ends.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        remaining = ends - now
        mins = max(0, int(remaining.total_seconds() // 60))
        timer_label = "Осталось" if lang == "ru" else "Remaining"
        text += f"\n⏱ {timer_label}: {mins} мин" if lang == "ru" else f"\n⏱ {timer_label}: {mins} min"

    # Add action buttons based on order status
    order_id = str(order["id"])
    active_rebowl = await has_active_rebowl(order_id) if status in ("SESSION_ACTIVE", "SESSION_ENDING") else False
    actions_kb = order_actions_keyboard(
        lang, status,
        free_extension_used=bool(order.get("free_extension_used")),
        has_active_rebowl=active_rebowl,
        after_hours=is_after_hours(),
    )
    await message.answer(text, reply_markup=actions_kb)


@router.message(F.text.in_({
    LABELS["support"]["ru"],
    LABELS["support"]["en"],
}))
async def btn_support(message: Message) -> None:
    """Handle 'Support' persistent button press.

    For now: acknowledge message, store in support_messages (Этап 3).
    """
    user = message.from_user
    if not user:
        return

    lang = await get_user_language(user.id)
    await message.answer(t("support_received", lang))


@router.message(F.text.in_({
    LABELS["open_app"]["ru"],
    LABELS["open_app"]["en"],
}))
async def btn_open_app(message: Message) -> None:
    """Handle 'Open App' button when WebApp is not available (no SSL).

    If SSL is set up, this won't trigger (WebApp opens directly).
    """
    user = message.from_user
    if not user:
        return

    lang = await get_user_language(user.id)
    if lang == "ru":
        text = "🏠 Откройте приложение по ссылке:\nhttp://164.68.109.12"
    else:
        text = "🏠 Open the app here:\nhttp://164.68.109.12"
    await message.answer(text)