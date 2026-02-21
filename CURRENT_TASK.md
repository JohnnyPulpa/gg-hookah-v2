# CURRENT_TASK.md

## F2.4: Mini App — Active Order Actions — DONE ✅

### What was done

1. **backend/app.py** — 2 new API endpoints:
   - `POST /api/orders/<id>/cancel` — cancels order (NEW/CONFIRMED/ON_THE_WAY only), writes audit_log, notifies bot
   - `POST /api/orders/<id>/ready-for-pickup` — marks WAITING_FOR_PICKUP (SESSION_ACTIVE/SESSION_ENDING only), writes audit_log, notifies bot
   - UUID validation on both endpoints
   - Fire-and-forget notification to bot via notification server (:5003)

2. **bot/services/notifications.py** — enhanced:
   - Added `WAITING_FOR_PICKUP` → `pickup_requested` template mapping
   - Added `ADMIN_NOTIFY_EVENTS` — miniapp actions now notify admin (cancel, ready for pickup)

3. **miniapp/src/api/orders.ts** — 2 new API functions:
   - `cancelOrder(orderId, telegramId)` → POST /api/orders/{id}/cancel
   - `readyForPickup(orderId, telegramId)` → POST /api/orders/{id}/ready-for-pickup

4. **miniapp/src/utils/translations.ts** — 8 new translation keys:
   - action_cancel_order, action_ready_pickup, action_confirm_cancel, action_confirm_cancel_yes/no
   - action_cancel_success, action_pickup_success, action_error

5. **miniapp/src/pages/Orders.tsx** — action buttons on active order:
   - Cancel button (red outline) — visible for NEW/CONFIRMED/ON_THE_WAY
   - Confirmation dialog before cancel ("Are you sure?")
   - Ready for Pickup button (green filled) — visible for SESSION_ACTIVE/SESSION_ENDING
   - Action loading state (disabled buttons)
   - Success/error message banner with auto-dismiss (4s)
   - Support button always visible
   - Auto-refresh orders after action

### Files created
- None

### Files modified
- `backend/app.py`
- `bot/services/notifications.py`
- `miniapp/src/api/orders.ts`
- `miniapp/src/utils/translations.ts`
- `miniapp/src/pages/Orders.tsx`

### Verified
- Bot restarted ✅ — no errors in logs
- API restarted ✅ — endpoints respond correctly
- Miniapp built ✅ — deployed to production
- Cancel endpoint validates UUID ✅
- Ready-for-pickup endpoint validates UUID ✅

## Статус: DONE

## Следующая задача: F2.5 — Multi-hookah Orders (корзина)
