"""
Admin Orders routes.
Spec 6.3: Active orders list with status badges, deposit info, flags.
Spec 6.4: Order detail with status transitions.
"""

import logging
import requests as http_requests
from flask import Blueprint, render_template, jsonify, request, session, redirect
from sqlalchemy import text
from admin.auth import login_required

log = logging.getLogger("gg-hookah-admin.orders")

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


# Status sort priority (spec 6.3)
STATUS_ORDER = {
    'SESSION_ENDING': 0,
    'WAITING_FOR_PICKUP': 1,
    'SESSION_ACTIVE': 2,
    'ON_THE_WAY': 3,
    'CONFIRMED': 4,
    'NEW': 5,
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


@orders_bp.route('/')
@login_required
def orders_list():
    """Render active orders list."""
    from admin.app import engine

    show_all = request.args.get('all', '0') == '1'

    if show_all:
        where_clause = "WHERE 1=1"
    else:
        where_clause = """
            WHERE o.status NOT IN ('COMPLETED', 'CANCELED')
        """

    query = text(f"""
        SELECT
            o.id,
            o.status,
            o.phone,
            o.hookah_count,
            o.address_text,
            o.deposit_type,
            o.deposit_amount_gel,
            o.promised_time,
            o.promised_eta_text,
            o.is_late_order,
            o.created_at,
            o.session_ends_at,
            o.comment,
            o.promo_code,
            o.discount_percent,
            o.promo_percent,
            m.name as mix_name,
            g.trust_flag,
            g.passport_photo_url
        FROM orders o
        LEFT JOIN mixes m ON o.mix_id = m.id
        LEFT JOIN guests g ON o.guest_id = g.id
        {where_clause}
        ORDER BY o.created_at DESC
        LIMIT 100
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()

    # Sort by status priority
    orders = []
    for row in rows:
        order = dict(row)
        order['status_priority'] = STATUS_ORDER.get(order['status'], 99)
        order['status_color'] = STATUS_COLORS.get(order['status'], '#7f8c8d')
        order['id_short'] = str(order['id'])[:8]

        # Remaining time for sessions
        if order.get('session_ends_at') and order['status'] in ('SESSION_ACTIVE', 'SESSION_ENDING'):
            from datetime import datetime, timezone
            ends = order['session_ends_at']
            if ends.tzinfo is None:
                ends = ends.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            remaining = ends - now
            order['remaining_min'] = max(0, int(remaining.total_seconds() // 60))
        else:
            order['remaining_min'] = None

        orders.append(order)

    # Sort by status priority, then created_at desc
    orders.sort(key=lambda x: (x['status_priority'], x['created_at'] or ''))

    return render_template('orders_list.html',
                           orders=orders,
                           show_all=show_all,
                           status_colors=STATUS_COLORS)
# --- Allowed transitions per status (spec 2.2 + 6.4.5) ---
ALLOWED_TRANSITIONS = {
    'NEW': ['CONFIRMED', 'CANCELED'],
    'CONFIRMED': ['ON_THE_WAY', 'CANCELED'],
    'ON_THE_WAY': ['DELIVERED'],
    'DELIVERED': ['SESSION_ACTIVE'],
    'SESSION_ACTIVE': ['SESSION_ENDING'],
    'SESSION_ENDING': ['WAITING_FOR_PICKUP', 'COMPLETED'],
    'WAITING_FOR_PICKUP': ['COMPLETED'],
    'COMPLETED': [],
    'CANCELED': [],
}

# Button labels per transition
TRANSITION_LABELS = {
    'CONFIRMED': '✅ Confirm',
    'ON_THE_WAY': '🚗 Set On The Way',
    'DELIVERED': '📦 Mark Delivered',
    'SESSION_ACTIVE': '⏱ Start Session',
    'SESSION_ENDING': '⚠️ Force Ending',
    'WAITING_FOR_PICKUP': '📦 Waiting for Pickup',
    'COMPLETED': '✅ Mark Completed',
    'CANCELED': '❌ Cancel Order',
}

TRANSITION_COLORS = {
    'CONFIRMED': '#2ecc71',
    'ON_THE_WAY': '#f39c12',
    'DELIVERED': '#9b59b6',
    'SESSION_ACTIVE': '#1abc9c',
    'SESSION_ENDING': '#e74c3c',
    'WAITING_FOR_PICKUP': '#e67e22',
    'COMPLETED': '#7f8c8d',
    'CANCELED': '#e74c3c',
}


@orders_bp.route('/<order_id>')
@login_required
def order_detail(order_id):
    """Full order detail screen (spec 6.4)."""
    from admin.app import engine

    query = text("""
        SELECT
            o.*,
            m.name as mix_name,
            m.flavors as mix_flavors,
            m.strength, m.coolness, m.sweetness, m.smokiness,
            g.name as guest_name,
            g.phone as guest_phone,
            g.trust_flag,
            g.passport_photo_url,
            g.notes as guest_notes
        FROM orders o
        LEFT JOIN mixes m ON o.mix_id = m.id
        LEFT JOIN guests g ON o.guest_id = g.id
        WHERE o.id = :oid
    """)

    with engine.connect() as conn:
        row = conn.execute(query, {'oid': order_id}).mappings().first()

        if not row:
            return "Order not found", 404

        order = dict(row)

        # Get order items (drinks)
        items = conn.execute(text("""
            SELECT oi.*, mi.name as item_name, mi.price_gel as item_price
            FROM order_items oi
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = :oid
        """), {'oid': order_id}).mappings().all()
        order['drinks'] = [dict(i) for i in items]

        # Get rebowl requests
        rebowls = conn.execute(text("""
            SELECT * FROM rebowl_requests
            WHERE order_id = :oid
            ORDER BY requested_at DESC
        """), {'oid': order_id}).mappings().all()
        order['rebowls'] = [dict(r) for r in rebowls]

    # Compute remaining time
    if order.get('session_ends_at') and order['status'] in ('SESSION_ACTIVE', 'SESSION_ENDING'):
        from datetime import datetime, timezone
        ends = order['session_ends_at']
        if ends.tzinfo is None:
            ends = ends.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        remaining = ends - now
        order['remaining_min'] = max(0, int(remaining.total_seconds() // 60))
    else:
        order['remaining_min'] = None

    order['id_short'] = str(order['id'])[:8]
    order['status_color'] = STATUS_COLORS.get(order['status'], '#7f8c8d')

    # Build available actions
    transitions = ALLOWED_TRANSITIONS.get(order['status'], [])
    actions = []
    for t in transitions:
        actions.append({
            'target_status': t,
            'label': TRANSITION_LABELS.get(t, t),
            'color': TRANSITION_COLORS.get(t, '#7f8c8d'),
            'confirm': t in ('CANCELED', 'COMPLETED', 'SESSION_ACTIVE'),
        })

    return render_template('order_detail.html',
                           order=order,
                           actions=actions,
                           status_colors=STATUS_COLORS)


# Map target order status → notification event
STATUS_TO_EVENT = {
    'CONFIRMED': 'ORDER_CONFIRMED',
    'ON_THE_WAY': 'ON_THE_WAY',
    'DELIVERED': 'DELIVERED',
    'SESSION_ACTIVE': 'SESSION_STARTED',
    'COMPLETED': 'ORDER_COMPLETED',
    'CANCELED': 'ORDER_CANCELED',
}


def _notify(event, telegram_id, order_id_short, **extra):
    """Fire-and-forget notification to bot notification server."""
    try:
        http_requests.post("http://127.0.0.1:5003/notify", json={
            "event": event,
            "telegram_id": telegram_id,
            "order_id_short": order_id_short,
            **extra,
        }, timeout=2)
    except Exception:
        log.debug("Notification send failed for event=%s", event, exc_info=True)


@orders_bp.route('/<order_id>/transition', methods=['POST'])
@login_required
def order_transition(order_id):
    """Change order status (spec 2.2)."""
    from admin.app import engine
    from datetime import datetime, timezone

    target = request.form.get('target_status')
    admin_id = session.get('admin_id')

    if not target:
        return jsonify({'error': 'Missing target_status'}), 400

    with engine.connect() as conn:
        # Get current order
        row = conn.execute(
            text("SELECT id, status, telegram_id FROM orders WHERE id = :oid"),
            {'oid': order_id}
        ).mappings().first()

        if not row:
            return jsonify({'error': 'Order not found'}), 404

        current = row['status']
        allowed = ALLOWED_TRANSITIONS.get(current, [])

        if target not in allowed:
            return jsonify({'error': f'Cannot transition from {current} to {target}'}), 400

        # Build update fields
        updates = ["status = :target", "updated_at = now()"]
        params = {'target': target, 'oid': order_id}

        if target == 'CONFIRMED':
            updates.append("confirmed_at = now()")
            eta = request.form.get('promised_eta_text', '')
            if eta:
                updates.append("promised_eta_text = :eta")
                params['eta'] = eta

        elif target == 'ON_THE_WAY':
            updates.append("departed_at = now()")

        elif target == 'DELIVERED':
            updates.append("delivered_at = now()")

        elif target == 'SESSION_ACTIVE':
            updates.append("session_started_at = now()")
            updates.append("session_ends_at = now() + interval '120 minutes'")
            updates.append("free_extension_used = false")

        elif target == 'CANCELED':
            updates.append("canceled_at = now()")

        set_clause = ", ".join(updates)
        conn.execute(text(f"UPDATE orders SET {set_clause} WHERE id = :oid"), params)

        # Audit log
        conn.execute(text("""
            INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
            VALUES ('order', :oid, :action, :details, :admin_id)
        """), {
            'oid': order_id,
            'action': f'STATUS_{current}_TO_{target}',
            'details': f'{{"from":"{current}","to":"{target}"}}',
            'admin_id': admin_id,
        })

        conn.commit()

    # Send notification (fire-and-forget)
    event = STATUS_TO_EVENT.get(target)
    tg_id = row['telegram_id']
    if event and tg_id:
        extra = {}
        if target == 'CONFIRMED':
            extra['eta_text'] = request.form.get('promised_eta_text', '')
        _notify(event, tg_id, str(order_id)[:8], **extra)

    return redirect(request.referrer or url_for('orders.order_detail', order_id=order_id))