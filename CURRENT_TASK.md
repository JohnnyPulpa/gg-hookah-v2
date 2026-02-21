# CURRENT_TASK.md

## F3.2: Settings Editor — DONE ✅

### What was done

1. **Seeded 8 new settings** (`backend/seed_settings.py`)
   - `event_min_hookahs`, `event_min_advance_hours`, `event_prepayment_percent`
   - `delivery_estimate_min`, `delivery_estimate_max`, `delivery_estimate_busy`
   - `first_order_discount`, `first_order_promo_code`
   - Total: 35 settings in DB

2. **Settings route** (`admin/routes/settings.py`)
   - `GET /settings/` — queries all settings, groups by 9 categories
   - `POST /settings/` — processes form, updates only changed values
   - Type detection: boolean (toggle), number, time, text
   - Correct boolean handling: hidden field + checkbox pattern with `getlist()`
   - Audit logging for every changed setting (entity_type='setting', key in details JSON)
   - Flash messages for success/info

3. **Settings template** (`admin/templates/settings.html`)
   - 9 collapsible groups: Business Hours, Pricing, Session, Inventory, Drinks, Discounts & Promos, Events, Delivery, Other
   - Type-aware inputs: toggles for booleans, number inputs, time inputs, text inputs
   - Monospace key names with descriptions
   - Dark theme, colored left borders per group
   - Sticky save button at bottom
   - Flash messages (green success, blue info)

4. **Wiring**
   - `admin/app.py` — registered settings_bp
   - `admin/templates/base.html` — sidebar link with active state

### Files created
- `admin/routes/settings.py`
- `admin/templates/settings.html`

### Files modified
- `admin/app.py` (blueprint registration)
- `admin/templates/base.html` (sidebar link)
- `backend/seed_settings.py` (8 new settings)

### Verified
- Admin service healthy ✅
- Settings page renders with all 35 settings in 9 groups ✅
- Save works: number and text changes persist ✅
- Boolean toggle works (checked → true, unchecked → false) ✅
- Audit logs created for changes ✅
- Git committed and pushed ✅

## Status: DONE

## Next task: F3.3 — Guests Management (CRM)
