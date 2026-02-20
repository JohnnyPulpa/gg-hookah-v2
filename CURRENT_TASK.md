# CURRENT_TASK.md

## F1.3: Session Timer Cron — DONE ✅

### What was done
1. Created `bot/services/session_timer.py` — asyncio background task (60s interval)
   - Queries orders: `status='SESSION_ACTIVE' AND session_ends_at <= now() + 30 min`
   - Transitions to `SESSION_ENDING` with race-condition protection (`WHERE status='SESSION_ACTIVE'` in UPDATE)
   - Inserts audit log: `AUTO_SESSION_ENDING`, `admin_telegram_id=0` (system)
   - Sends notification via existing `send_notification()` → resolves `session_ending_before_02` or `session_ending_after_02` based on Tbilisi time
   - Entire tick wrapped in try/except — one failure doesn't kill the loop
2. Modified `bot/bot_main.py` — `asyncio.create_task(session_timer_loop(bot))` after notification server start

### Files created
- `bot/services/session_timer.py`

### Files modified
- `bot/bot_main.py`

### Verified
- Bot starts with "Session timer cron started (interval=60s)" in logs ✅
- Timer ticks every 60 seconds ✅
- Test: set order to SESSION_ACTIVE with session_ends_at=now()+10min → auto-transitioned to SESSION_ENDING within 60s ✅
- Audit log entry created with action=AUTO_SESSION_ENDING ✅
- Notification attempted (gracefully handles missing user) ✅
- Timer continues running after errors ✅

## Статус: DONE

## Следующая задача: уточнить у пользователя
