"""
Admin Settings Editor — F3.2.
Single-page grouped settings with type-aware inputs.
"""

import json
import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy import text
from admin.auth import login_required

log = logging.getLogger("gg-hookah-admin.settings")

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

# --- Category definitions (order matters) ---
CATEGORIES = [
    {
        'id': 'hours',
        'name': 'Business Hours',
        'icon': '🕐',
        'color': '#3498db',
        'keys': [
            'work_days', 'work_start', 'work_end', 'timezone',
            'late_order_cutoff_time', 'after_hours_disable_time',
        ],
    },
    {
        'id': 'pricing',
        'name': 'Pricing',
        'icon': '💰',
        'color': '#2ecc71',
        'keys': ['base_bowl_price', 'rebowl_price', 'deposit_amount'],
    },
    {
        'id': 'session',
        'name': 'Session',
        'icon': '⏱',
        'color': '#1abc9c',
        'keys': [
            'session_duration', 'rebowl_duration',
            'free_extension', 'free_extension_max_uses',
        ],
    },
    {
        'id': 'inventory',
        'name': 'Inventory',
        'icon': '🔥',
        'color': '#9b59b6',
        'keys': [
            'total_hookahs', 'max_hookahs_regular', 'max_hookahs_event',
            'pause_orders', 'pause_reason_text',
        ],
    },
    {
        'id': 'drinks',
        'name': 'Drinks',
        'icon': '🥤',
        'color': '#e67e22',
        'keys': ['drinks_enabled', 'drinks_max_total_qty'],
    },
    {
        'id': 'discounts',
        'name': 'Discounts & Promos',
        'icon': '🎟',
        'color': '#F28C18',
        'keys': [
            'discount_hookah_only', 'promo_enabled', 'promo_per_phone_limit',
            'first_order_discount', 'first_order_promo_code',
        ],
    },
    {
        'id': 'events',
        'name': 'Events',
        'icon': '🎉',
        'color': '#e74c3c',
        'keys': [
            'event_min_hookahs', 'event_min_advance_hours',
            'event_prepayment_percent',
        ],
    },
    {
        'id': 'delivery',
        'name': 'Delivery',
        'icon': '🚗',
        'color': '#f39c12',
        'keys': [
            'delivery_estimate_min', 'delivery_estimate_max',
            'delivery_estimate_busy',
        ],
    },
    {
        'id': 'other',
        'name': 'Other',
        'icon': '⚙️',
        'color': '#8892a4',
        'keys': [
            'board_games_enabled', 'board_games_available_now',
            'passport_retention_days', 'default_language',
        ],
    },
]

# --- Type detection ---
BOOLEAN_KEYS = {
    'drinks_enabled', 'discount_hookah_only', 'promo_enabled',
    'pause_orders', 'board_games_enabled', 'board_games_available_now',
}

TIME_KEYS = {
    'work_start', 'work_end', 'late_order_cutoff_time',
    'after_hours_disable_time',
}

NUMBER_KEYS = {
    'base_bowl_price', 'rebowl_price', 'deposit_amount',
    'session_duration', 'rebowl_duration', 'free_extension',
    'free_extension_max_uses', 'drinks_max_total_qty',
    'promo_per_phone_limit', 'total_hookahs',
    'max_hookahs_regular', 'max_hookahs_event',
    'event_min_hookahs', 'event_min_advance_hours',
    'event_prepayment_percent', 'passport_retention_days',
    'delivery_estimate_min', 'delivery_estimate_max',
    'delivery_estimate_busy', 'first_order_discount',
}


def _get_type(key):
    """Determine input type for a setting key."""
    if key in BOOLEAN_KEYS:
        return 'boolean'
    if key in TIME_KEYS:
        return 'time'
    if key in NUMBER_KEYS:
        return 'number'
    return 'text'


def _audit_log(conn, key, action, details, admin_id):
    """Insert audit log entry for setting change."""
    conn.execute(text("""
        INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
        VALUES ('setting', NULL, :action, :details, :admin_id)
    """), {
        'action': action,
        'details': details,
        'admin_id': admin_id,
    })


@settings_bp.route('/')
@login_required
def settings_list():
    """Render all settings grouped by category."""
    from admin.app import engine

    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT key, value, description, updated_at FROM settings ORDER BY key"
        )).mappings().all()

    # Build lookup
    settings_map = {r['key']: dict(r) for r in rows}

    # Build grouped data for template
    groups = []
    for cat in CATEGORIES:
        items = []
        for key in cat['keys']:
            s = settings_map.get(key)
            if s:
                s['input_type'] = _get_type(key)
                items.append(s)
        if items:
            groups.append({
                'id': cat['id'],
                'name': cat['name'],
                'icon': cat['icon'],
                'color': cat['color'],
                'settings': items,
            })

    # Any settings not in a category
    categorized_keys = set()
    for cat in CATEGORIES:
        categorized_keys.update(cat['keys'])
    uncategorized = [
        {**dict(r), 'input_type': _get_type(r['key'])}
        for r in rows if r['key'] not in categorized_keys
    ]
    if uncategorized:
        groups.append({
            'id': 'uncategorized',
            'name': 'Uncategorized',
            'icon': '❓',
            'color': '#5a6270',
            'settings': uncategorized,
        })

    return render_template('settings.html', groups=groups)


@settings_bp.route('/', methods=['POST'])
@login_required
def settings_save():
    """Process settings form and update changed values."""
    from admin.app import engine

    admin_id = session.get('admin_id')
    changed = 0

    with engine.connect() as conn:
        # Get current values
        rows = conn.execute(text(
            "SELECT key, value FROM settings"
        )).mappings().all()
        current = {r['key']: r['value'] for r in rows}

        # Collect unique keys from form (skip boolean keys — handled separately)
        seen_keys = set()
        for form_key in request.form:
            if not form_key.startswith('s__'):
                continue
            key = form_key[3:]
            if key in BOOLEAN_KEYS or key in seen_keys:
                continue
            seen_keys.add(key)

            old_value = current.get(key)
            if old_value is None:
                continue

            new_value = request.form.get(form_key, '').strip()
            if old_value != new_value:
                conn.execute(text("""
                    UPDATE settings
                    SET value = :val,
                        updated_at = now(),
                        updated_by_admin_telegram_id = :admin_id
                    WHERE key = :key
                """), {'val': new_value, 'key': key, 'admin_id': admin_id})

                _audit_log(conn, key, 'SETTING_UPDATED',
                           json.dumps({'key': key, 'from': old_value, 'to': new_value}),
                           admin_id)
                changed += 1

        # Handle booleans: checkbox sends hidden "false" + checked "true"
        for key in BOOLEAN_KEYS:
            if key not in current:
                continue
            form_key = f's__{key}'
            # getlist returns all values; if "true" is among them, checkbox was checked
            values = request.form.getlist(form_key)
            new_value = 'true' if 'true' in values else 'false'
            old_value = current[key]

            if old_value != new_value:
                conn.execute(text("""
                    UPDATE settings
                    SET value = :val,
                        updated_at = now(),
                        updated_by_admin_telegram_id = :admin_id
                    WHERE key = :key
                """), {'val': new_value, 'key': key, 'admin_id': admin_id})
                _audit_log(conn, key, 'SETTING_UPDATED',
                           json.dumps({'key': key, 'from': old_value, 'to': new_value}),
                           admin_id)
                changed += 1

        conn.commit()

    if changed:
        flash(f'Saved {changed} setting{"s" if changed != 1 else ""}.', 'success')
    else:
        flash('No changes detected.', 'info')

    return redirect(url_for('settings.settings_list'))
