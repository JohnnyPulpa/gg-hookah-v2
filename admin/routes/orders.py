"""
Admin Orders routes.
Spec 6.3: Active orders list with status badges, deposit info, flags.
Spec 6.4: Order detail with status transitions.
"""

from flask import Blueprint, render_template, jsonify, request, session
from sqlalchemy import text
from admin.auth import login_required

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
@orders_bp.route('/<order_id>')
@login_required
def order_detail(order_id):
    """Order detail — stub, will be built in M7.4."""
    return f"<h2>Order detail: {order_id}</h2><p>Coming in M7.4</p><a href='{request.url_root}orders/'>← Back</a>"