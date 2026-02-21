"""
Admin Dashboard route — F3.1.
Single-screen overview: widgets, kanban board, charts, alerts.
"""

import logging
from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, session
from sqlalchemy import text
from admin.auth import login_required

log = logging.getLogger("gg-hookah-admin.dashboard")

dashboard_bp = Blueprint('dashboard', __name__)

# Kanban columns in flow order
KANBAN_STATUSES = [
    'NEW', 'CONFIRMED', 'ON_THE_WAY', 'DELIVERED',
    'SESSION_ACTIVE', 'WAITING_FOR_PICKUP',
]

KANBAN_LABELS = {
    'NEW': 'New',
    'CONFIRMED': 'Confirmed',
    'ON_THE_WAY': 'On the Way',
    'DELIVERED': 'Delivered',
    'SESSION_ACTIVE': 'Session',
    'WAITING_FOR_PICKUP': 'Pickup',
}

STATUS_COLORS = {
    'NEW': '#3498db',
    'CONFIRMED': '#2ecc71',
    'ON_THE_WAY': '#f39c12',
    'DELIVERED': '#9b59b6',
    'SESSION_ACTIVE': '#1abc9c',
    'SESSION_ENDING': '#e74c3c',
    'WAITING_FOR_PICKUP': '#e67e22',
    'COMPLETED': '#7f8c8d',
    'CANCELED': '#95a5a6',
}

# Quick action: what button to show on each kanban card
QUICK_ACTIONS = {
    'NEW': {'target': 'CONFIRMED', 'label': 'Confirm', 'icon': '✅', 'color': '#2ecc71'},
    'CONFIRMED': {'target': 'ON_THE_WAY', 'label': 'Ship', 'icon': '🚗', 'color': '#f39c12'},
    'ON_THE_WAY': {'target': 'DELIVERED', 'label': 'Delivered', 'icon': '📦', 'color': '#9b59b6'},
    'DELIVERED': {'target': 'SESSION_ACTIVE', 'label': 'Start', 'icon': '⏱', 'color': '#1abc9c'},
    'SESSION_ACTIVE': None,
    'WAITING_FOR_PICKUP': {'target': 'COMPLETED', 'label': 'Complete', 'icon': '✅', 'color': '#2ecc71'},
}


def _get_setting(conn, key, default=None):
    """Read a single setting from the settings table."""
    row = conn.execute(
        text("SELECT value FROM settings WHERE key = :k"),
        {"k": key},
    ).fetchone()
    return row[0] if row else default


def _time_ago(dt):
    """Return human-readable time ago string."""
    if not dt:
        return ''
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = now - dt
    minutes = int(diff.total_seconds() // 60)
    if minutes < 1:
        return 'just now'
    if minutes < 60:
        return f'{minutes}m ago'
    hours = minutes // 60
    if hours < 24:
        return f'{hours}h ago'
    return f'{hours // 24}d ago'


@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard — single-screen overview."""
    from admin.app import engine

    with engine.connect() as conn:
        # --- 1. Widget: Today's orders count + revenue ---
        today_stats = conn.execute(text("""
            SELECT
                COUNT(DISTINCT o.id) as cnt,
                COALESCE(SUM(oi.total_price_gel), 0) as revenue
            FROM orders o
            LEFT JOIN order_items oi ON oi.order_id = o.id
            WHERE o.created_at::date = CURRENT_DATE
              AND o.status != 'CANCELED'
        """)).mappings().first()

        # --- 2. Widget: Live (active) orders ---
        live_count = conn.execute(text("""
            SELECT COUNT(*) as cnt FROM orders
            WHERE status NOT IN ('COMPLETED', 'CANCELED')
        """)).scalar()

        # --- 3. Widget: Active sessions ---
        sessions_count = conn.execute(text("""
            SELECT COUNT(*) as cnt FROM orders
            WHERE status IN ('SESSION_ACTIVE', 'SESSION_ENDING')
        """)).scalar()

        # --- 4. Widget: Available hookahs ---
        total_hookahs = int(_get_setting(conn, 'total_hookahs', '5'))
        rented_hookahs = conn.execute(text("""
            SELECT COALESCE(SUM(hookah_count), 0) FROM orders
            WHERE status IN (
                'CONFIRMED', 'ON_THE_WAY', 'DELIVERED',
                'SESSION_ACTIVE', 'SESSION_ENDING', 'WAITING_FOR_PICKUP'
            )
        """)).scalar()
        available_hookahs = max(0, total_hookahs - int(rented_hookahs))

        # --- 5. Kanban: Active orders ---
        kanban_rows = conn.execute(text("""
            SELECT
                o.id, o.status, o.phone, o.hookah_count,
                o.address_text, o.created_at, o.session_ends_at,
                o.comment, o.deposit_type,
                g.trust_flag, g.name as guest_name
            FROM orders o
            LEFT JOIN guests g ON o.guest_id = g.id
            WHERE o.status NOT IN ('COMPLETED', 'CANCELED')
            ORDER BY o.created_at ASC
        """)).mappings().all()

        # Get order items (mixes) for each active order
        order_mixes = {}
        if kanban_rows:
            mix_rows = conn.execute(text("""
                SELECT oi.order_id, m.name as mix_name, oi.quantity
                FROM order_items oi
                JOIN mixes m ON oi.mix_id = m.id
                WHERE oi.item_type = 'hookah'
                  AND oi.order_id IN (
                      SELECT id FROM orders
                      WHERE status NOT IN ('COMPLETED', 'CANCELED')
                  )
                ORDER BY oi.created_at
            """)).mappings().all()
            for mr in mix_rows:
                oid = str(mr['order_id'])
                if oid not in order_mixes:
                    order_mixes[oid] = []
                qty_str = f' x{mr["quantity"]}' if mr['quantity'] > 1 else ''
                order_mixes[oid].append(f'{mr["mix_name"]}{qty_str}')

        # --- 6. Chart: Revenue per day (last 7 days) ---
        revenue_rows = conn.execute(text("""
            SELECT d::date as day,
                   COALESCE(SUM(oi.total_price_gel), 0) as revenue
            FROM generate_series(
                CURRENT_DATE - INTERVAL '6 days',
                CURRENT_DATE,
                '1 day'
            ) d
            LEFT JOIN orders o ON o.created_at::date = d::date
                AND o.status != 'CANCELED'
            LEFT JOIN order_items oi ON oi.order_id = o.id
            GROUP BY d::date
            ORDER BY d::date
        """)).mappings().all()

        # --- 7. Chart: Top mixes (all time, top 5) ---
        top_mixes = conn.execute(text("""
            SELECT m.name, COUNT(*) as cnt
            FROM order_items oi
            JOIN mixes m ON oi.mix_id = m.id
            WHERE oi.item_type = 'hookah'
            GROUP BY m.name
            ORDER BY cnt DESC
            LIMIT 5
        """)).mappings().all()

        # --- 8. Alerts: Overdue sessions ---
        overdue = conn.execute(text("""
            SELECT o.id, o.phone, o.session_ends_at, o.address_text,
                   g.name as guest_name
            FROM orders o
            LEFT JOIN guests g ON o.guest_id = g.id
            WHERE o.status IN ('SESSION_ACTIVE', 'SESSION_ENDING')
              AND o.session_ends_at < now()
        """)).mappings().all()

        # --- 9. Alerts: Low trust guests with active orders ---
        low_trust = conn.execute(text("""
            SELECT o.id, o.phone, g.trust_flag, g.name as guest_name
            FROM orders o
            JOIN guests g ON o.guest_id = g.id
            WHERE o.status NOT IN ('COMPLETED', 'CANCELED')
              AND g.trust_flag = 'low'
        """)).mappings().all()

    # Build kanban columns
    now = datetime.now(timezone.utc)
    kanban = {s: [] for s in KANBAN_STATUSES}
    for row in kanban_rows:
        order = dict(row)
        status = order['status']
        # SESSION_ENDING orders go into SESSION_ACTIVE column
        col = status if status in KANBAN_STATUSES else 'SESSION_ACTIVE'
        order['id_short'] = str(order['id'])[:8]
        order['time_ago'] = _time_ago(order['created_at'])
        order['mixes_display'] = order_mixes.get(str(order['id']), ['—'])

        # Remaining time for sessions
        if order.get('session_ends_at') and status in ('SESSION_ACTIVE', 'SESSION_ENDING'):
            ends = order['session_ends_at']
            if ends.tzinfo is None:
                ends = ends.replace(tzinfo=timezone.utc)
            remaining = ends - now
            order['remaining_min'] = max(0, int(remaining.total_seconds() // 60))
            order['is_overdue'] = remaining.total_seconds() < 0
        else:
            order['remaining_min'] = None
            order['is_overdue'] = False

        order['quick_action'] = QUICK_ACTIONS.get(status)
        order['status_color'] = STATUS_COLORS.get(status, '#7f8c8d')
        kanban[col].append(order)

    # Chart data
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    chart_revenue = {
        'labels': [day_names[r['day'].weekday()] for r in revenue_rows],
        'data': [int(r['revenue']) for r in revenue_rows],
    }

    mix_colors = ['#F28C18', '#2ecc71', '#3498db', '#9b59b6', '#e74c3c']
    chart_mixes = {
        'labels': [r['name'] for r in top_mixes],
        'data': [int(r['cnt']) for r in top_mixes],
        'colors': mix_colors[:len(top_mixes)],
    }

    # Alerts
    alerts = {
        'overdue': [{
            'id': str(r['id'])[:8],
            'full_id': str(r['id']),
            'phone': r['phone'],
            'guest_name': r['guest_name'] or '—',
            'address': (r['address_text'] or '')[:40],
            'overdue_min': max(0, int((now - (
                r['session_ends_at'].replace(tzinfo=timezone.utc)
                if r['session_ends_at'] and r['session_ends_at'].tzinfo is None
                else r['session_ends_at']
            )).total_seconds() // 60)) if r['session_ends_at'] else 0,
        } for r in overdue],
        'low_trust': [{
            'id': str(r['id'])[:8],
            'full_id': str(r['id']),
            'phone': r['phone'],
            'guest_name': r['guest_name'] or '—',
        } for r in low_trust],
    }

    widgets = {
        'live_orders': live_count or 0,
        'today_revenue': int(today_stats['revenue']) if today_stats else 0,
        'orders_today': int(today_stats['cnt']) if today_stats else 0,
        'active_sessions': sessions_count or 0,
        'hookahs_available': available_hookahs,
        'hookahs_total': total_hookahs,
    }

    return render_template('dashboard.html',
                           widgets=widgets,
                           kanban=kanban,
                           kanban_statuses=KANBAN_STATUSES,
                           kanban_labels=KANBAN_LABELS,
                           status_colors=STATUS_COLORS,
                           chart_revenue=chart_revenue,
                           chart_mixes=chart_mixes,
                           alerts=alerts,
                           total_active=live_count or 0)
