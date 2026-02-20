# CURRENT_TASK.md

## F1.2: Notification Service (Admin → Bot → User) — DONE ✅

### What was done
1. Created `bot/services/notifications.py` — event→template mapping, language-aware message formatting via `bot.templates.t()`
2. Created `bot/notification_server.py` — aiohttp server on `127.0.0.1:5003` with `POST /notify` and `GET /health`
3. Modified `bot/bot_main.py` — starts notification server before polling (same asyncio loop)
4. Modified `admin/routes/orders.py` — `_notify()` fire-and-forget after each order status transition
5. Modified `admin/routes/sessions.py` — `_notify()` for session actions (force_ending, complete, free_extend) and rebowl transitions (IN_PROGRESS, DONE)
6. Configured Claude Code: `.claude/settings.json`, 4 slash commands, auto-commit rules in `CLAUDE.md`

### Event mapping
| Admin action | Notification event | Template |
|---|---|---|
| Order → CONFIRMED | ORDER_CONFIRMED | order_confirmed |
| Order → ON_THE_WAY | ON_THE_WAY | order_on_the_way |
| Order → DELIVERED | DELIVERED | order_delivered |
| Order → SESSION_ACTIVE | SESSION_STARTED | session_started |
| Order → COMPLETED | ORDER_COMPLETED | order_completed |
| Order → CANCELED | ORDER_CANCELED | order_canceled |
| Session → force_ending | SESSION_ENDING | session_ending_before/after_02 |
| Session → complete | ORDER_COMPLETED | order_completed |
| Session → free_extend | FREE_EXTENSION | free_extension_used |
| Rebowl → IN_PROGRESS | REBOWL_IN_PROGRESS | rebowl_on_the_way |
| Rebowl → DONE | REBOWL_DONE | rebowl_done |

### Files created
- `bot/notification_server.py`
- `bot/services/__init__.py`
- `bot/services/notifications.py`
- `.claude/settings.json`
- `.claude/commands/deploy-miniapp.md`
- `.claude/commands/restart-all.md`
- `.claude/commands/check-health.md`
- `.claude/commands/end-of-day.md`

### Files modified
- `bot/bot_main.py`
- `admin/routes/orders.py`
- `admin/routes/sessions.py`
- `CLAUDE.md`

### Verified
- `sudo systemctl restart gg-hookah-bot` — OK, notification server starts on :5003
- `curl http://127.0.0.1:5003/health` → `{"status": "ok"}`
- `curl -X POST /notify` → `{"ok": true}` (sends notification, gracefully handles missing user)
- `sudo systemctl restart gg-hookah-admin` — OK
- `curl http://127.0.0.1:5002/health` → `{"status": "ok"}`

## Статус: DONE

## Следующая задача: F1.3 (по roadmap)
