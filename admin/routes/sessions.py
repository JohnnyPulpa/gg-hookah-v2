"""
Admin Sessions routes.
Spec 6.5: Sessions list & detail — active hookahs at guests.
Sessions = orders with status SESSION_ACTIVE / SESSION_ENDING / WAITING_FOR_PICKUP.
"""

import logging
import requests as http_requests
from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from sqlalchemy import text
from admin.auth import login_required
from datetime import datetime, timezone

log = logging.getLogger("gg-hookah-admin.sessions")

sessions_bp = Blueprint('sessions', __name__, url_prefix='/sessions')

# Status sort priority for sessions (spec 6.5.1)
SESSION_STATUS_ORDER = {
    'SESSION_ENDING': 0,
    'WAITING_FOR_PICKUP': 1,
    'SESSION_ACTIVE': 2,
}

STATUS_COLORS = {
    'SESSION_ACTIVE': '#1abc9c',
    'SESSION_ENDING': '#e74c3c',
    'WAITING_FOR_PICKUP': '#e67e22',
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


def _compute_remaining(session_ends_at, status):
    """Compute remaining minutes for a session."""
    if not session_ends_at or status not in ('SESSION_ACTIVE', 'SESSION_ENDING', 'WAITING_FOR_PICKUP'):
        return None
    ends = session_ends_at
    if ends.tzinfo is None:
        ends = ends.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    remaining = ends - now
    return max(0, int(remaining.total_seconds() // 60))


@sessions_bp.route('/')
@login_required
def sessions_list():
    """Render active sessions list (spec 6.5.1)."""
    from admin.app import engine

    query = text("""
        SELECT
            o.id,
            o.status,
            o.phone,
            o.hookah_count,
            o.address_text,
            o.deposit_type,
            o.deposit_amount_gel,
            o.session_started_at,
            o.session_ends_at,
            o.free_extension_used,
            o.created_at,
            m.name as mix_name,
            g.name as guest_name,
            g.trust_flag,
            g.passport_photo_url,
            (SELECT count(*) FROM rebowl_requests r WHERE r.order_id = o.id) as rebowl_count,
            (SELECT count(*) FROM rebowl_requests r
             WHERE r.order_id = o.id AND r.status IN ('REQUESTED', 'IN_PROGRESS')) as active_rebowl
        FROM orders o
        LEFT JOIN mixes m ON o.mix_id = m.id
        LEFT JOIN guests g ON o.guest_id = g.id
        WHERE o.status IN ('SESSION_ACTIVE', 'SESSION_ENDING', 'WAITING_FOR_PICKUP')
        ORDER BY o.session_ends_at ASC NULLS LAST
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()

    sessions_data = []
    for row in rows:
        s = dict(row)
        s['remaining_min'] = _compute_remaining(s.get('session_ends_at'), s['status'])
        s['status_priority'] = SESSION_STATUS_ORDER.get(s['status'], 99)
        s['status_color'] = STATUS_COLORS.get(s['status'], '#7f8c8d')
        s['id_short'] = str(s['id'])[:8]
        sessions_data.append(s)

    # Sort: SESSION_ENDING first, then WAITING, then ACTIVE
    sessions_data.sort(key=lambda x: (x['status_priority'], x.get('session_ends_at') or datetime.max.replace(tzinfo=timezone.utc)))

    return render_template('sessions_list.html',
                           sessions=sessions_data,
                           status_colors=STATUS_COLORS)


@sessions_bp.route('/<session_id>')
@login_required
def session_detail(session_id):
    """Session detail screen (spec 6.5.2)."""
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
        row = conn.execute(query, {'oid': session_id}).mappings().first()
        if not row:
            return "Session not found", 404

        order = dict(row)

        # Get rebowl requests
        rebowls = conn.execute(text("""
            SELECT r.*, mx.name as rebowl_mix_name
            FROM rebowl_requests r
            LEFT JOIN mixes mx ON r.mix_id = mx.id
            WHERE r.order_id = :oid
            ORDER BY r.requested_at DESC
        """), {'oid': session_id}).mappings().all()
        order['rebowls'] = [dict(r) for r in rebowls]

        # Get order items (drinks)
        items = conn.execute(text("""
            SELECT oi.*, mi.name as item_name, mi.price_gel as item_price
            FROM order_items oi
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = :oid
        """), {'oid': session_id}).mappings().all()
        order['drinks'] = [dict(i) for i in items]

    order['remaining_min'] = _compute_remaining(order.get('session_ends_at'), order['status'])
    order['id_short'] = str(order['id'])[:8]
    order['status_color'] = STATUS_COLORS.get(order['status'], '#7f8c8d')

    # Check if free extension is available (spec 3.8)
    # Available only in SESSION_ENDING, before 02:00, not yet used
    import pytz
    tz = pytz.timezone('Asia/Tbilisi')
    now_local = datetime.now(tz)
    after_hours = now_local.hour >= 2 and now_local.hour < 18  # between 02:00 and 18:00

    can_free_extend = (
        order['status'] == 'SESSION_ENDING'
        and not order.get('free_extension_used')
        and not after_hours
    )

    # Check if rebowl can be requested (before 02:00, no active rebowl)
    has_active_rebowl = any(
        r['status'] in ('REQUESTED', 'IN_PROGRESS')
        for r in order['rebowls']
    )
    can_rebowl = (
        order['status'] in ('SESSION_ENDING', 'WAITING_FOR_PICKUP')
        and not after_hours
        and not has_active_rebowl
    )

    # Build actions
    actions = []
    if order['status'] == 'SESSION_ACTIVE':
        actions.append({
            'action': 'force_ending',
            'label': '⚠️ Force SESSION_ENDING',
            'color': '#e74c3c',
            'confirm': True,
        })
    if order['status'] in ('SESSION_ENDING', 'WAITING_FOR_PICKUP'):
        actions.append({
            'action': 'complete',
            'label': '✅ Mark COMPLETED',
            'color': '#2ecc71',
            'confirm': True,
        })
    if order['status'] == 'WAITING_FOR_PICKUP' and not after_hours and not has_active_rebowl:
        # Spec: WAITING_FOR_PICKUP → SESSION_ACTIVE if rebowl DONE
        # Admin can also manually restart session
        pass

    return render_template('session_detail.html',
                           order=order,
                           actions=actions,
                           can_free_extend=can_free_extend,
                           can_rebowl=can_rebowl,
                           has_active_rebowl=has_active_rebowl,
                           after_hours=after_hours,
                           status_colors=STATUS_COLORS)


@sessions_bp.route('/<session_id>/action', methods=['POST'])
@login_required
def session_action(session_id):
    """Handle session actions: force_ending, complete, free_extend, adjust_timer."""
    from admin.app import engine

    action = request.form.get('action')
    admin_id = session.get('admin_id')

    if not action:
        return jsonify({'error': 'Missing action'}), 400

    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, status, session_ends_at, free_extension_used, telegram_id FROM orders WHERE id = :oid"),
            {'oid': session_id}
        ).mappings().first()

        if not row:
            return jsonify({'error': 'Session not found'}), 404

        order = dict(row)

        if action == 'force_ending':
            if order['status'] != 'SESSION_ACTIVE':
                return jsonify({'error': 'Can only force ending from SESSION_ACTIVE'}), 400

            conn.execute(text("""
                UPDATE orders SET status = 'SESSION_ENDING', updated_at = now()
                WHERE id = :oid
            """), {'oid': session_id})

            _audit_log(conn, session_id, 'FORCE_SESSION_ENDING',
                       '{"action":"admin forced SESSION_ENDING"}', admin_id)

        elif action == 'complete':
            if order['status'] not in ('SESSION_ENDING', 'WAITING_FOR_PICKUP', 'SESSION_ACTIVE'):
                return jsonify({'error': 'Cannot complete from this status'}), 400

            conn.execute(text("""
                UPDATE orders SET status = 'COMPLETED', completed_at = now(), updated_at = now()
                WHERE id = :oid
            """), {'oid': session_id})

            _audit_log(conn, session_id, 'ORDER_COMPLETED',
                       f'{{"from":"{order["status"]}"}}', admin_id)

        elif action == 'free_extend':
            if order['status'] != 'SESSION_ENDING':
                return jsonify({'error': 'Free extension only from SESSION_ENDING'}), 400
            if order.get('free_extension_used'):
                return jsonify({'error': 'Free extension already used'}), 400

            conn.execute(text("""
                UPDATE orders
                SET status = 'SESSION_ACTIVE',
                    session_ends_at = session_ends_at + interval '60 minutes',
                    free_extension_used = true,
                    updated_at = now()
                WHERE id = :oid
            """), {'oid': session_id})

            _audit_log(conn, session_id, 'FREE_EXTENSION_USED',
                       '{"minutes":60}', admin_id)

        elif action == 'adjust_timer':
            minutes = request.form.get('minutes', type=int)
            if not minutes:
                return jsonify({'error': 'Missing minutes'}), 400

            conn.execute(text("""
                UPDATE orders
                SET session_ends_at = session_ends_at + make_interval(mins => :mins),
                    updated_at = now()
                WHERE id = :oid
            """), {'oid': session_id, 'mins': minutes})

            _audit_log(conn, session_id, 'TIMER_ADJUSTED',
                       f'{{"minutes":{minutes}}}', admin_id)

        else:
            return jsonify({'error': f'Unknown action: {action}'}), 400

        conn.commit()

    # Send notification (fire-and-forget)
    tg_id = order.get('telegram_id')
    id_short = str(session_id)[:8]
    if tg_id:
        if action == 'force_ending':
            _notify('SESSION_ENDING', tg_id, id_short)
        elif action == 'complete':
            _notify('ORDER_COMPLETED', tg_id, id_short)
        elif action == 'free_extend':
            _notify('FREE_EXTENSION', tg_id, id_short)

    return redirect(url_for('sessions.session_detail', session_id=session_id))


@sessions_bp.route('/<session_id>/rebowl/<rebowl_id>/transition', methods=['POST'])
@login_required
def rebowl_transition(session_id, rebowl_id):
    """Handle rebowl status transitions (spec 6.5.2).
    REQUESTED → IN_PROGRESS → DONE/CANCELED
    DONE: session_ends_at = now + 120m, order status → SESSION_ACTIVE
    """
    from admin.app import engine

    target = request.form.get('target_status')
    admin_id = session.get('admin_id')

    REBOWL_TRANSITIONS = {
        'REQUESTED': ['IN_PROGRESS', 'CANCELED'],
        'IN_PROGRESS': ['DONE', 'CANCELED'],
    }

    if not target:
        return jsonify({'error': 'Missing target_status'}), 400

    with engine.connect() as conn:
        rebowl = conn.execute(
            text("SELECT * FROM rebowl_requests WHERE id = :rid AND order_id = :oid"),
            {'rid': rebowl_id, 'oid': session_id}
        ).mappings().first()

        if not rebowl:
            return jsonify({'error': 'Rebowl request not found'}), 404

        # Get telegram_id for notification
        order_row = conn.execute(
            text("SELECT telegram_id FROM orders WHERE id = :oid"),
            {'oid': session_id}
        ).mappings().first()

        allowed = REBOWL_TRANSITIONS.get(rebowl['status'], [])
        if target not in allowed:
            return jsonify({'error': f'Cannot transition rebowl from {rebowl["status"]} to {target}'}), 400

        # Update rebowl
        if target == 'IN_PROGRESS':
            conn.execute(text("""
                UPDATE rebowl_requests
                SET status = 'IN_PROGRESS', in_progress_at = now()
                WHERE id = :rid
            """), {'rid': rebowl_id})

        elif target == 'DONE':
            # Mark rebowl done
            conn.execute(text("""
                UPDATE rebowl_requests
                SET status = 'DONE', done_at = now()
                WHERE id = :rid
            """), {'rid': rebowl_id})

            # Reset session: status → SESSION_ACTIVE, session_ends_at = now + 120m (spec 6.5.2)
            conn.execute(text("""
                UPDATE orders
                SET status = 'SESSION_ACTIVE',
                    session_ends_at = now() + interval '120 minutes',
                    updated_at = now()
                WHERE id = :oid
            """), {'oid': session_id})

            # Update guest total_rebowls
            conn.execute(text("""
                UPDATE guests SET total_rebowls = total_rebowls + 1, updated_at = now()
                WHERE id = (SELECT guest_id FROM orders WHERE id = :oid)
            """), {'oid': session_id})

        elif target == 'CANCELED':
            conn.execute(text("""
                UPDATE rebowl_requests
                SET status = 'CANCELED', canceled_at = now(), admin_note = :note
                WHERE id = :rid
            """), {'rid': rebowl_id, 'note': request.form.get('admin_note', '')})

        # Audit log
        _audit_log(conn, session_id,
                   f'REBOWL_{target}',
                   f'{{"rebowl_id":"{rebowl_id}","from":"{rebowl["status"]}","to":"{target}"}}',
                   admin_id)

        conn.commit()

    # Send notification (fire-and-forget)
    tg_id = order_row['telegram_id'] if order_row else None
    id_short = str(session_id)[:8]
    if tg_id:
        if target == 'IN_PROGRESS':
            _notify('REBOWL_IN_PROGRESS', tg_id, id_short)
        elif target == 'DONE':
            _notify('REBOWL_DONE', tg_id, id_short)

    return redirect(url_for('sessions.session_detail', session_id=session_id))


def _audit_log(conn, entity_id, action, details, admin_id):
    """Insert audit log entry."""
    conn.execute(text("""
        INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
        VALUES ('order', :eid, :action, :details, :admin_id)
    """), {
        'eid': entity_id,
        'action': action,
        'details': details,
        'admin_id': admin_id,
    })