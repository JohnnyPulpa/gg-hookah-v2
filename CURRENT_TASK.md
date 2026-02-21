# CURRENT_TASK.md

## F3.3: Guests Management (CRM) — DONE ✅

### What was done

1. **Guests route** (`admin/routes/guests.py`)
   - `GET /guests/` — list with search (phone/name ILIKE) and trust filter tabs (All/Normal/Low/Blacklist)
   - `GET /guests/<id>` — detail with aggregated metrics (total_spent, favorite_mix), order history
   - `POST /guests/<id>/update` — edit name, trust_flag, notes with audit logging
   - Trust flags: normal (🟢), low (🟡), blacklist (🔴) with colored badges

2. **Guests list template** (`admin/templates/guests_list.html`)
   - Search bar + trust filter tabs
   - Table: Guest (name + phone), Telegram, Trust badge, Orders, Spent (₾), Last Order, Passport
   - Clickable rows → guest detail
   - Empty state

3. **Guest detail template** (`admin/templates/guest_detail.html`)
   - Stats cards: Orders, Total Spent, Rebowls, Favorite Mix
   - Guest info block: phone, telegram_id, passport status, member since, last order
   - Edit form: name input, trust level radio buttons (visual selection), notes textarea
   - Order history table with status badges, clickable to order detail
   - Flash messages for save feedback

4. **Wiring**
   - `admin/app.py` — registered guests_bp
   - `admin/templates/base.html` — sidebar link with active state

### Files created
- `admin/routes/guests.py`
- `admin/templates/guests_list.html`
- `admin/templates/guest_detail.html`

### Files modified
- `admin/app.py` (blueprint registration)
- `admin/templates/base.html` (sidebar link)

### Verified
- Guests list renders with data ✅
- Search by phone works ✅
- Trust filter works ✅
- Guest detail renders with stats + order history ✅
- Update name/trust/notes persists + creates audit log ✅
- Git committed and pushed ✅

## Status: DONE

## Next task: F3.4 — Discounts & Promo Codes
