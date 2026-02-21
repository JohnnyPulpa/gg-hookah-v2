# CURRENT_TASK.md

## F2.2: Bot Hot Actions — Free +1h, Rebowl Request — DONE ✅

### What was done

1. **bot/db.py** — added 5 new functions:
   - `is_after_hours()` — checks 02:00-18:00 Tbilisi time restriction
   - `apply_free_extension(order_id, telegram_id)` — extends session +1h, sets free_extension_used=true
   - `has_active_rebowl(order_id)` — checks for REQUESTED/IN_PROGRESS rebowl
   - `create_rebowl_request(order_id, telegram_id, mix_id)` — creates rebowl with REQUESTED status (50₾, +120min)
   - Expanded `get_active_order()` to include free_extension_used and mix_id

2. **bot/templates.py** — added 2 admin notification templates:
   - `admin_client_free_extend` — notifies admin when client extends session
   - `admin_client_rebowl` — notifies admin when client requests rebowl

3. **bot/keyboards/main.py** — expanded `order_actions_keyboard()` with new params:
   - `free_extension_used`, `has_active_rebowl`, `after_hours`
   - SESSION_ENDING + before 02:00 → shows: +1h free, New bowl 50₾, Ready for pickup
   - SESSION_ACTIVE → shows: Ready for pickup
   - Buttons hidden when conditions not met (extension used, active rebowl, after hours)

4. **bot/handlers/session_actions.py** — NEW FILE with 2 callback handlers:
   - `action:free_extend` → validates (SESSION_ENDING + not used + before 02:00) → extends session
   - `action:rebowl` → validates (session status + before 02:00 + no active rebowl) → creates request

5. **bot/handlers/start.py** — My Order handler now passes smart flags to keyboard
6. **bot/services/notifications.py** — SESSION_ENDING notifications fetch order data for smart buttons
7. **bot/bot_main.py** — registered session_actions_router

### Files created
- `bot/handlers/session_actions.py`

### Files modified
- `bot/db.py`
- `bot/templates.py`
- `bot/keyboards/main.py`
- `bot/handlers/start.py`
- `bot/services/notifications.py`
- `bot/bot_main.py`

### Verified
- Bot restarted successfully ✅
- No errors in logs ✅
- Notification server running on :5003 ✅
- Session timer cron running ✅

## Статус: DONE

## Следующая задача: F2.3 — Support Routing
