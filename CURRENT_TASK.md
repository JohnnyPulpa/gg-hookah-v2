# CURRENT_TASK.md

## F2.3: Support Routing — DONE ✅

### What was done

1. **bot/db.py** — added `save_support_message()`:
   - Inserts into support_messages with direction='CLIENT_TO_ADMIN'
   - Params: telegram_id, text, thread_type, thread_id

2. **bot/templates.py** — added 3 templates:
   - `support_prompt` — "Напишите ваше сообщение, ответим в течение 15 минут"
   - `support_received` — updated text to match spec (15 minutes)
   - `admin_support_message` — notification with client name, thread type, message text

3. **bot/handlers/support.py** — NEW FILE:
   - Catch-all `F.text` handler (lowest priority — registered last)
   - Determines thread_type: session (SESSION_ACTIVE/SESSION_ENDING), order (any active), general (none)
   - Saves message to support_messages via db helper
   - Replies to client with "support_received" template
   - Notifies all ADMIN_IDS with message details

4. **bot/handlers/start.py** — updated `btn_support()`:
   - Now sends `support_prompt` (write your message) instead of `support_received`
   - Next text message caught by catch-all handler in support.py

5. **bot/bot_main.py** — registered support_router LAST

### Files created
- `bot/handlers/support.py`

### Files modified
- `bot/db.py`
- `bot/templates.py`
- `bot/handlers/start.py`
- `bot/bot_main.py`

### Verified
- Bot restarted successfully ✅
- No errors in logs ✅
- Notification server running on :5003 ✅
- Session timer cron running ✅

## Статус: DONE

## Следующая задача: F2.4 — Mini App: Active Order Actions
