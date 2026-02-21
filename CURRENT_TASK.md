# CURRENT_TASK.md

## F3.1: Admin Dashboard (Full Redesign) — DONE ✅

### What was done

1. **Dashboard route** (`admin/routes/dashboard.py`)
   - New blueprint with `GET /` route replacing old redirect
   - Queries: today revenue + count, live orders, active sessions, available hookahs
   - Kanban data: active orders grouped by status with mix names from order_items
   - Charts: revenue last 7 days (with generate_series for zero-fill), top 5 mixes
   - Alerts: overdue sessions, low-trust guests with active orders

2. **Dashboard template** (`admin/templates/dashboard.html`)
   - **5 widget cards**: Live Orders, Today Revenue, Orders Today, Active Sessions, Hookahs Available
   - **Kanban board**: 6 columns (NEW → CONFIRMED → ON_THE_WAY → DELIVERED → SESSION_ACTIVE → WAITING_FOR_PICKUP)
   - Kanban cards show: order ID, time ago, mix names, hookah count, phone, deposit type, trust flag
   - **Quick action buttons** on each card (Confirm, Ship, Delivered, Start Session, Complete)
   - Quick actions POST to existing `/orders/<id>/transition` endpoint
   - **Revenue bar chart** (Chart.js, last 7 days) with orange theme
   - **Top mixes doughnut chart** (Chart.js, all-time top 5)
   - **Alerts section**: overdue sessions (red), low trust guests (yellow)
   - **Auto-refresh**: 60-second countdown with page reload
   - **New order notification**: beep sound (Web Audio API) + browser notification when order count increases
   - Session timer display on kanban cards with overdue animation
   - Dark theme matching existing admin panel

3. **Wiring**
   - `admin/app.py`: registered dashboard_bp, removed old redirect route
   - `admin/templates/base.html`: added Dashboard as first sidebar link
   - `admin/auth.py`: updated login redirect to `dashboard.index`

### Files created
- `admin/routes/dashboard.py`

### Files modified
- `admin/templates/dashboard.html` (full rewrite)
- `admin/templates/base.html` (sidebar link + logo link)
- `admin/app.py` (blueprint registration, removed old route)
- `admin/auth.py` (login redirect)

### Verified
- Admin service restarted ✅ — health check 200
- Dashboard renders with all sections ✅
- All widget data queries execute correctly ✅
- Git committed and pushed ✅

## Status: DONE

## Next task: F3.2 — Settings Editor
