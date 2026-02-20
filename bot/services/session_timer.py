"""Session timer cron — auto-transitions SESSION_ACTIVE → SESSION_ENDING.

Runs as asyncio background task inside the bot process.
Every 60 seconds, checks for orders where session_ends_at is within 30 minutes
and transitions them to SESSION_ENDING with audit log + user notification.
"""

import asyncio
import logging
from aiogram import Bot
from sqlalchemy import text
from bot.db import engine
from bot.services.notifications import send_notification

log = logging.getLogger("gg-hookah-bot.session-timer")

TICK_INTERVAL = 60  # seconds


def _transition_expiring_sessions() -> list[tuple[str, int]]:
    """Find SESSION_ACTIVE orders expiring within 30 min, transition them.

    Returns list of (order_id, telegram_id) for notification.
    Runs synchronously (called via run_in_executor).
    """
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id, telegram_id
            FROM orders
            WHERE status = 'SESSION_ACTIVE'
              AND session_ends_at <= now() + interval '30 minutes'
        """)).mappings().all()

        if not rows:
            return []

        transitioned = []
        for row in rows:
            oid = row["id"]
            # Use WHERE status check to prevent race with admin panel
            result = conn.execute(text("""
                UPDATE orders
                SET status = 'SESSION_ENDING', updated_at = now()
                WHERE id = :oid AND status = 'SESSION_ACTIVE'
            """), {"oid": oid})

            if result.rowcount > 0:
                conn.execute(text("""
                    INSERT INTO audit_logs
                        (entity_type, entity_id, action, details, admin_telegram_id)
                    VALUES
                        ('order', :oid, 'AUTO_SESSION_ENDING',
                         '{"trigger":"timer_cron"}', 0)
                """), {"oid": oid})
                transitioned.append((str(oid), row["telegram_id"]))

        conn.commit()
        return transitioned


async def session_timer_loop(bot: Bot) -> None:
    """Background task: check for expiring sessions every 60 seconds."""
    log.info("Session timer cron started (interval=%ds)", TICK_INTERVAL)

    while True:
        try:
            await asyncio.sleep(TICK_INTERVAL)

            loop = asyncio.get_event_loop()
            transitioned = await loop.run_in_executor(
                None, _transition_expiring_sessions
            )

            for order_id, telegram_id in transitioned:
                log.info(
                    "Auto SESSION_ENDING: order=%s telegram_id=%s",
                    order_id[:8], telegram_id,
                )
                await send_notification(
                    bot, "SESSION_ENDING", telegram_id,
                    {"order_id_short": order_id[:8]},
                )

        except asyncio.CancelledError:
            log.info("Session timer cron stopped")
            break
        except Exception:
            log.exception("Session timer tick failed")
