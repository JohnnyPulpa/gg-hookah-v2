# CURRENT_TASK.md

## F1.1: Admin Template Inheritance — DONE

### What was done
1. Created `admin/templates/base.html` — shared layout with sidebar, topbar, styles, scripts
2. Converted all 9 templates to `{% extends "base.html" %}` with `{% block content %}`, `{% block title %}`, `{% block sidebar_active %}`, `{% block extra_styles %}`, `{% block extra_scripts %}`
3. **B22 FIXED**: sidebar Menu link now uses `{{ url_for('menu.mixes_list') }}` instead of `#`
4. Sidebar active state via `{% block sidebar_active %}orders/sessions/menu{% endblock %}` + `self.sidebar_active()|trim` comparison
5. `login.html` left unchanged (no sidebar)

### Files changed
- `admin/templates/base.html` (NEW)
- `admin/templates/dashboard.html` (refactored)
- `admin/templates/orders_list.html` (refactored)
- `admin/templates/order_detail.html` (refactored)
- `admin/templates/sessions_list.html` (refactored)
- `admin/templates/session_detail.html` (refactored)
- `admin/templates/menu_mixes.html` (refactored)
- `admin/templates/menu_mix_form.html` (refactored)
- `admin/templates/menu_drinks.html` (refactored)
- `admin/templates/menu_drink_form.html` (refactored)

### Verified
- `sudo systemctl restart gg-hookah-admin` — OK
- `curl http://127.0.0.1:5002/health` — `{"status": "ok"}`
- All pages return 302 (redirect to login) — no template errors
- No errors in journalctl logs
