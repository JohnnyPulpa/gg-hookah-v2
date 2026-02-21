"""Async database helpers for the bot.

Uses synchronous SQLAlchemy with run_in_executor for simplicity,
since bot DB calls are infrequent (no need for full async driver).
"""

import asyncio
from datetime import datetime
from functools import partial
from sqlalchemy import create_engine, text
import pytz
from bot.config import DATABASE_URL

# Create engine once (shared across bot lifetime)
engine = create_engine(DATABASE_URL, pool_size=5, pool_pre_ping=True)


def _execute_sync(query: str, params: dict | None = None) -> list[dict]:
    """Execute a SQL query synchronously, return list of row dicts."""
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        # UPDATE/INSERT/DELETE don't return rows
        if result.returns_rows:
            rows = result.mappings().all()
            return [dict(r) for r in rows]
        conn.commit()
        return []


async def execute(query: str, params: dict | None = None) -> list[dict]:
    """Run a sync DB query in executor (non-blocking for asyncio)."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(_execute_sync, query, params))


async def get_user_language(telegram_id: int) -> str:
    """Get user language preference. Default: 'ru'."""
    rows = await execute(
        "SELECT language FROM users WHERE telegram_id = :tid LIMIT 1",
        {"tid": telegram_id},
    )
    if rows:
        return rows[0].get("language", "ru") or "ru"
    return "ru"


def is_after_hours() -> bool:
    """Check if current Tbilisi time is between 02:00 and 18:00 (no extensions/rebowl)."""
    tz = pytz.timezone("Asia/Tbilisi")
    now_local = datetime.now(tz)
    return 2 <= now_local.hour < 18


async def get_active_order(telegram_id: int) -> dict | None:
    """Get active order for a telegram user (not COMPLETED/CANCELED)."""
    rows = await execute(
        """
        SELECT o.id, o.status, o.address_text, o.phone,
               o.hookah_count, o.created_at, o.session_ends_at,
               o.free_extension_used, o.mix_id,
               m.name as mix_name
        FROM orders o
        LEFT JOIN mixes m ON m.id = o.mix_id
        WHERE o.telegram_id = :tid
          AND o.status NOT IN ('COMPLETED', 'CANCELED')
        ORDER BY o.created_at DESC
        LIMIT 1
        """,
        {"tid": telegram_id},
    )
    return rows[0] if rows else None


async def cancel_order(order_id: str, telegram_id: int) -> bool:
    """Cancel an order (client action). Returns True if successful."""
    rows = await execute(
        """
        UPDATE orders
        SET status = 'CANCELED', canceled_at = now(), updated_at = now()
        WHERE id = :oid
          AND telegram_id = :tid
          AND status IN ('NEW', 'CONFIRMED', 'ON_THE_WAY')
        RETURNING id
        """,
        {"oid": order_id, "tid": telegram_id},
    )
    if rows:
        await execute(
            """
            INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
            VALUES ('order', :oid, 'CLIENT_CANCEL', '{"source":"telegram_bot"}', :tid)
            """,
            {"oid": order_id, "tid": telegram_id},
        )
        return True
    return False


async def set_ready_for_pickup(order_id: str, telegram_id: int) -> bool:
    """Client signals ready for pickup. Returns True if successful."""
    rows = await execute(
        """
        UPDATE orders
        SET status = 'WAITING_FOR_PICKUP', pickup_requested_at = now(), updated_at = now()
        WHERE id = :oid
          AND telegram_id = :tid
          AND status IN ('SESSION_ACTIVE', 'SESSION_ENDING')
        RETURNING id
        """,
        {"oid": order_id, "tid": telegram_id},
    )
    if rows:
        await execute(
            """
            INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
            VALUES ('order', :oid, 'CLIENT_READY_PICKUP', '{"source":"telegram_bot"}', :tid)
            """,
            {"oid": order_id, "tid": telegram_id},
        )
        return True
    return False


async def get_user_name(telegram_id: int) -> str:
    """Get user display name for admin notifications."""
    rows = await execute(
        "SELECT first_name, username FROM users WHERE telegram_id = :tid LIMIT 1",
        {"tid": telegram_id},
    )
    if rows:
        name = rows[0].get("first_name", "")
        username = rows[0].get("username", "")
        if name:
            return f"{name} (@{username})" if username else name
        if username:
            return f"@{username}"
    return str(telegram_id)


async def apply_free_extension(order_id: str, telegram_id: int) -> bool:
    """Apply free +1h extension (client action). Returns True if successful."""
    rows = await execute(
        """
        UPDATE orders
        SET status = 'SESSION_ACTIVE',
            session_ends_at = session_ends_at + interval '60 minutes',
            free_extension_used = true,
            updated_at = now()
        WHERE id = :oid
          AND telegram_id = :tid
          AND status = 'SESSION_ENDING'
          AND free_extension_used = false
        RETURNING id
        """,
        {"oid": order_id, "tid": telegram_id},
    )
    if rows:
        await execute(
            """
            INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
            VALUES ('order', :oid, 'CLIENT_FREE_EXTENSION', '{"source":"telegram_bot","minutes":60}', :tid)
            """,
            {"oid": order_id, "tid": telegram_id},
        )
        return True
    return False


async def has_active_rebowl(order_id: str) -> bool:
    """Check if order has an active rebowl request (REQUESTED or IN_PROGRESS)."""
    rows = await execute(
        """
        SELECT 1 FROM rebowl_requests
        WHERE order_id = :oid
          AND status IN ('REQUESTED', 'IN_PROGRESS')
        LIMIT 1
        """,
        {"oid": order_id},
    )
    return bool(rows)


async def create_rebowl_request(order_id: str, telegram_id: int, mix_id: str) -> bool:
    """Create a rebowl request (client action). Returns True if successful."""
    # Check no active rebowl first
    if await has_active_rebowl(order_id):
        return False

    rows = await execute(
        """
        INSERT INTO rebowl_requests (order_id, requested_by_telegram_id, mix_id, price_gel, add_minutes, status)
        VALUES (:oid, :tid, :mid, 50, 120, 'REQUESTED')
        RETURNING id
        """,
        {"oid": order_id, "tid": telegram_id, "mid": mix_id},
    )
    if rows:
        await execute(
            """
            INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
            VALUES ('rebowl_request', :rid, 'CLIENT_REBOWL_REQUEST', :details, :tid)
            """,
            {"rid": str(rows[0]["id"]), "details": f'{{"source":"telegram_bot","order_id":"{order_id}"}}', "tid": telegram_id},
        )
        return True
    return False


async def save_support_message(
    telegram_id: int, text: str, thread_type: str, thread_id: str | None = None
) -> None:
    """Save a support message from client to DB."""
    await execute(
        """
        INSERT INTO support_messages (telegram_user_id, text, thread_type, thread_id, direction)
        VALUES (:tid, :text, :ttype, :thread_id, 'CLIENT_TO_ADMIN')
        """,
        {
            "tid": telegram_id,
            "text": text,
            "ttype": thread_type,
            "thread_id": thread_id,
        },
    )


async def ensure_user_exists(telegram_id: int, first_name: str = "",
                              last_name: str = "", username: str = "") -> None:
    """Create user record if not exists (upsert)."""
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO users (telegram_id, first_name, last_name, username, language)
            VALUES (:tid, :fn, :ln, :un, 'ru')
            ON CONFLICT (telegram_id) DO UPDATE
            SET first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                username = EXCLUDED.username,
                updated_at = now()
        """), {"tid": telegram_id, "fn": first_name, "ln": last_name, "un": username})
        conn.commit()