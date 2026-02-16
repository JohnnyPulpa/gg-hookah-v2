"""Async database helpers for the bot.

Uses synchronous SQLAlchemy with run_in_executor for simplicity,
since bot DB calls are infrequent (no need for full async driver).
"""

import asyncio
from functools import partial
from sqlalchemy import create_engine, text
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


async def get_active_order(telegram_id: int) -> dict | None:
    """Get active order for a telegram user (not COMPLETED/CANCELED)."""
    rows = await execute(
        """
        SELECT o.id, o.status, o.address_text, o.phone,
               o.hookah_count, o.created_at, o.session_ends_at,
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