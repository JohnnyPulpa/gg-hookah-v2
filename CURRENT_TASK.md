# CURRENT_TASK.md

## F2.1: Bot Hot Actions — Cancel, Ready for Pickup — DONE ✅

### What was done

1. **bot/db.py** — added 3 new async helpers:
   - `cancel_order(order_id, telegram_id)` — cancels order (only NEW/CONFIRMED/ON_THE_WAY), writes audit log
   - `set_ready_for_pickup(order_id, telegram_id)` — transitions to WAITING_FOR_PICKUP (only SESSION_ACTIVE/SESSION_ENDING), writes audit log
   - `get_user_name(telegram_id)` — returns display name for admin notifications

2. **bot/templates.py** — added 2 admin notification templates:
   - `admin_client_cancel` — notifies admin when client cancels
   - `admin_client_ready_pickup` — notifies admin when client is ready for pickup

3. **bot/keyboards/main.py** — added `order_actions_keyboard(lang, status)`:
   - NEW/CONFIRMED/ON_THE_WAY → "❌ Cancel order" button
   - SESSION_ACTIVE/SESSION_ENDING → "📦 Ready for pickup" button
   - Other statuses → no buttons

4. **bot/handlers/order_actions.py** — NEW FILE, router with 4 callback handlers:
   - `action:cancel` → shows confirmation dialog
   - `confirm_cancel_yes` → cancels order, notifies admin
   - `confirm_cancel_no` → dismisses dialog
   - `action:ready_pickup` → transitions to WAITING_FOR_PICKUP, notifies admin

5. **bot/handlers/start.py** — "My Order" handler now shows inline action buttons

6. **bot/services/notifications.py** — notification messages now include action buttons:
   - ORDER_CONFIRMED, ON_THE_WAY → Cancel button
   - SESSION_STARTED, SESSION_ENDING → Ready for pickup button

7. **bot/bot_main.py** — registered order_actions_router

### Files created
- `bot/handlers/order_actions.py`

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

## Следующая задача: F2.2 — Bot Hot Actions: Free +1h, Rebowl Request
