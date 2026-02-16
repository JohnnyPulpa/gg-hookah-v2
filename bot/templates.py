"""Message templates RU/EN for all bot events.

Based on Spec Section 5.7. Each template is a dict with 'ru' and 'en' keys.
"""

TEMPLATES = {
    # --- /start greeting ---
    "welcome": {
        "ru": (
            "👋 Привет! Я бот GG HOOKAH.\n\n"
            "Заказывайте кальян через приложение, "
            "а здесь я помогу с поддержкой и уведомлениями."
        ),
        "en": (
            "👋 Hi! I'm the GG HOOKAH bot.\n\n"
            "Order hookah through the app, "
            "and I'll help you with support and notifications here."
        ),
    },

    # --- Order status notifications (Spec 5.7) ---
    "order_created": {
        "ru": (
            "✅ Заказ #{order_id_short} получен.\n"
            "Мы свяжемся по телефону, чтобы подтвердить детали и время."
        ),
        "en": (
            "✅ Order #{order_id_short} received.\n"
            "We'll call you to confirm details and timing."
        ),
    },
    "order_confirmed": {
        "ru": "📋 Заказ #{order_id_short} подтверждён. {eta_text}",
        "en": "📋 Order #{order_id_short} confirmed. {eta_text}",
    },
    "order_on_the_way": {
        "ru": (
            "🚗 Мы выехали! Заказ #{order_id_short}.\n"
            "Если что-то изменилось — напишите в поддержку."
        ),
        "en": (
            "🚗 We're on the way! Order #{order_id_short}.\n"
            "If anything changed — contact support."
        ),
    },
    "order_delivered": {
        "ru": "🎉 Кальян установлен. Приятного отдыха!",
        "en": "🎉 Hookah is set up. Enjoy!",
    },
    "session_started": {
        "ru": (
            "⏱ Сессия началась! Заказ #{order_id_short}.\n\n"
            "За 30 минут до окончания мы напомним и предложим варианты:\n"
            "• Вернуть кальян\n"
            "• Продлить возврат на 1 час (бесплатно)\n"
            "• Заказать новую чашу (+2 часа, 50₾)"
        ),
        "en": (
            "⏱ Session started! Order #{order_id_short}.\n\n"
            "We'll remind you 30 min before it ends with options:\n"
            "• Return the hookah\n"
            "• Extend return by 1 hour (free)\n"
            "• Order a new bowl (+2 hours, 50₾)"
        ),
    },
    "session_ending_before_02": {
        "ru": (
            "⚠️ Осталось 30 минут! Заказ #{order_id_short}.\n\n"
            "Выберите:\n"
            "🔄 Новая чаша (+2 часа, 50₾)\n"
            "⏰ Продлить возврат на 1 час (бесплатно)\n"
            "📦 Готов отдать кальян"
        ),
        "en": (
            "⚠️ 30 minutes left! Order #{order_id_short}.\n\n"
            "Choose:\n"
            "🔄 New bowl (+2 hours, 50₾)\n"
            "⏰ Extend return by 1 hour (free)\n"
            "📦 Ready for pickup"
        ),
    },
    "session_ending_after_02": {
        "ru": (
            "⚠️ Осталось 30 минут. Заказ #{order_id_short}.\n\n"
            "Мы работаем до 02:00. Продления и новая чаша "
            "сейчас недоступны.\n\n"
            "📦 Нажмите «Готов отдать» или напишите в поддержку."
        ),
        "en": (
            "⚠️ 30 minutes left. Order #{order_id_short}.\n\n"
            "We work until 02:00. Extensions and new bowl "
            "are unavailable right now.\n\n"
            "📦 Tap 'Ready for pickup' or contact support."
        ),
    },
    "pickup_requested": {
        "ru": "📦 Принято. Скоро будем, мы с вами свяжемся.",
        "en": "📦 Received. We'll be there soon, we'll contact you.",
    },
    "order_completed": {
        "ru": (
            "🙏 Спасибо! Заказ #{order_id_short} завершён.\n"
            "Если захотите снова — оформляйте через приложение."
        ),
        "en": (
            "🙏 Thank you! Order #{order_id_short} completed.\n"
            "Want another one? Order through the app."
        ),
    },
    "order_canceled": {
        "ru": "❌ Заказ #{order_id_short} отменён. Оформите новый в приложении, когда захотите.",
        "en": "❌ Order #{order_id_short} canceled. Place a new one in the app whenever you want.",
    },
    "discount_issued": {
        "ru": (
            "🎁 Вам выдана скидка {percent}%!\n"
            "Действует до {expires}. Применится автоматически "
            "к следующему заказу кальяна."
        ),
        "en": (
            "🎁 You got a {percent}% discount!\n"
            "Valid until {expires}. It will be applied automatically "
            "to your next hookah order."
        ),
    },

    # --- Rebowl ---
    "rebowl_requested": {
        "ru": "🔄 Запрос на новую чашу принят. Ожидайте, мы скоро будем!",
        "en": "🔄 New bowl request received. We'll be there soon!",
    },
    "rebowl_on_the_way": {
        "ru": "🚗 Выезжаем заменить чашу!",
        "en": "🚗 On the way to replace the bowl!",
    },
    "rebowl_done": {
        "ru": "✅ Чаша заменена! Сессия продлена на 2 часа. Приятного отдыха!",
        "en": "✅ Bowl replaced! Session extended by 2 hours. Enjoy!",
    },
    "rebowl_canceled": {
        "ru": "❌ Запрос на новую чашу отменён.",
        "en": "❌ New bowl request canceled.",
    },

    # --- Free extension ---
    "free_extension_used": {
        "ru": "⏰ Возврат продлён на 1 час бесплатно!",
        "en": "⏰ Return extended by 1 hour for free!",
    },

    # --- Support ---
    "support_received": {
        "ru": "💬 Сообщение получено. Мы ответим в ближайшее время.",
        "en": "💬 Message received. We'll reply soon.",
    },

    # --- Errors / info ---
    "no_active_order": {
        "ru": "У вас нет активного заказа. Оформите через приложение!",
        "en": "You don't have an active order. Place one through the app!",
    },
    "help": {
        "ru": (
            "📖 Доступные действия:\n\n"
            "🏠 Открыть приложение — заказать кальян\n"
            "📋 Мой заказ — статус активного заказа\n"
            "💬 Поддержка — написать нам"
        ),
        "en": (
            "📖 Available actions:\n\n"
            "🏠 Open app — order hookah\n"
            "📋 My order — active order status\n"
            "💬 Support — message us"
        ),
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Get a translated template string.

    Usage: t("order_created", "en", order_id_short="abc123")
    """
    template = TEMPLATES.get(key, {})
    text = template.get(lang, template.get("ru", f"[missing template: {key}]"))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass  # Return template as-is if format fails
    return text