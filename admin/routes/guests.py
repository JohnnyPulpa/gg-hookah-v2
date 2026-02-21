"""
Admin Guests Management (CRM) — F3.3.
List, detail, edit for guest profiles with order history.
"""

import json
import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy import text
from admin.auth import login_required

log = logging.getLogger("gg-hookah-admin.guests")

guests_bp = Blueprint('guests', __name__, url_prefix='/guests')

TRUST_FLAGS = ['normal', 'low', 'blacklist']

TRUST_COLORS = {
    'normal': '#2ecc71',
    'low': '#f39c12',
    'blacklist': '#e74c3c',
}

TRUST_ICONS = {
    'normal': '🟢',
    'low': '🟡',
    'blacklist': '🔴',
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


def _audit_log(conn, entity_id, action, details, admin_id):
    """Insert audit log entry."""
    conn.execute(text("""
        INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
        VALUES ('guest', :eid, :action, :details, :admin_id)
    """), {
        'eid': entity_id,
        'action': action,
        'details': details,
        'admin_id': admin_id,
    })


@guests_bp.route('/')
@login_required
def guests_list():
    """List all guests with search and trust filter."""
    from admin.app import engine

    q = request.args.get('q', '').strip()
    trust = request.args.get('trust', 'all')

    # Build WHERE conditions
    conditions = []
    params = {}

    if q:
        conditions.append("(g.phone ILIKE :q OR g.name ILIKE :q)")
        params['q'] = f'%{q}%'

    if trust and trust != 'all':
        conditions.append("g.trust_flag = :trust")
        params['trust'] = trust

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = text(f"""
        SELECT
            g.id, g.phone, g.telegram_id, g.name,
            g.trust_flag, g.passport_photo_url, g.notes,
            g.total_orders, g.total_rebowls,
            g.created_at,
            COALESCE(SUM(oi.total_price_gel), 0) as total_spent,
            MAX(o.created_at) as last_order_at
        FROM guests g
        LEFT JOIN orders o ON o.guest_id = g.id AND o.status != 'CANCELED'
        LEFT JOIN order_items oi ON oi.order_id = o.id
        {where}
        GROUP BY g.id
        ORDER BY g.created_at DESC
    """)

    with engine.connect() as conn:
        rows = conn.execute(query, params).mappings().all()

    guests = []
    for row in rows:
        g = dict(row)
        g['id_short'] = str(g['id'])[:8]
        g['trust_color'] = TRUST_COLORS.get(g['trust_flag'], '#8892a4')
        g['trust_icon'] = TRUST_ICONS.get(g['trust_flag'], '⚪')
        guests.append(g)

    return render_template('guests_list.html',
                           guests=guests,
                           search_q=q,
                           trust_filter=trust,
                           trust_colors=TRUST_COLORS,
                           trust_icons=TRUST_ICONS)


@guests_bp.route('/<guest_id>')
@login_required
def guest_detail(guest_id):
    """Guest detail with stats, edit form, and order history."""
    from admin.app import engine

    with engine.connect() as conn:
        # Guest info with aggregated metrics
        row = conn.execute(text("""
            SELECT
                g.*,
                COALESCE(SUM(oi.total_price_gel), 0) as total_spent,
                MAX(o.created_at) as last_order_at
            FROM guests g
            LEFT JOIN orders o ON o.guest_id = g.id AND o.status != 'CANCELED'
            LEFT JOIN order_items oi ON oi.order_id = o.id
            WHERE g.id = :gid
            GROUP BY g.id
        """), {'gid': guest_id}).mappings().first()

        if not row:
            return "Guest not found", 404

        guest = dict(row)

        # Favorite mix
        fav = conn.execute(text("""
            SELECT m.name, COUNT(*) as cnt
            FROM order_items oi
            JOIN mixes m ON oi.mix_id = m.id
            WHERE oi.item_type = 'hookah'
              AND oi.order_id IN (SELECT id FROM orders WHERE guest_id = :gid)
            GROUP BY m.name
            ORDER BY cnt DESC
            LIMIT 1
        """), {'gid': guest_id}).mappings().first()
        guest['favorite_mix'] = fav['name'] if fav else None

        # Order history
        orders = conn.execute(text("""
            SELECT
                o.id, o.status, o.phone, o.hookah_count,
                o.address_text, o.deposit_type, o.deposit_amount_gel,
                o.created_at, o.session_ends_at,
                m.name as mix_name
            FROM orders o
            LEFT JOIN mixes m ON o.mix_id = m.id
            WHERE o.guest_id = :gid
            ORDER BY o.created_at DESC
        """), {'gid': guest_id}).mappings().all()

        order_list = []
        for o in orders:
            od = dict(o)
            od['id_short'] = str(od['id'])[:8]
            od['status_color'] = STATUS_COLORS.get(od['status'], '#7f8c8d')
            order_list.append(od)

    guest['id_short'] = str(guest['id'])[:8]
    guest['trust_color'] = TRUST_COLORS.get(guest['trust_flag'], '#8892a4')
    guest['trust_icon'] = TRUST_ICONS.get(guest['trust_flag'], '⚪')

    return render_template('guest_detail.html',
                           guest=guest,
                           orders=order_list,
                           trust_flags=TRUST_FLAGS,
                           trust_colors=TRUST_COLORS,
                           trust_icons=TRUST_ICONS,
                           status_colors=STATUS_COLORS)


@guests_bp.route('/<guest_id>/update', methods=['POST'])
@login_required
def guest_update(guest_id):
    """Update guest name, trust_flag, notes."""
    from admin.app import engine

    admin_id = session.get('admin_id')
    name = request.form.get('name', '').strip()
    trust_flag = request.form.get('trust_flag', 'normal')
    notes = request.form.get('notes', '').strip()

    if trust_flag not in TRUST_FLAGS:
        trust_flag = 'normal'

    with engine.connect() as conn:
        # Get current values
        current = conn.execute(text(
            "SELECT name, trust_flag, notes FROM guests WHERE id = :gid"
        ), {'gid': guest_id}).mappings().first()

        if not current:
            return "Guest not found", 404

        changes = {}
        if (name or None) != (current['name'] or None):
            changes['name'] = {'from': current['name'], 'to': name or None}
        if trust_flag != current['trust_flag']:
            changes['trust_flag'] = {'from': current['trust_flag'], 'to': trust_flag}
        if (notes or None) != (current['notes'] or None):
            changes['notes'] = {'from': current['notes'], 'to': notes or None}

        if changes:
            conn.execute(text("""
                UPDATE guests
                SET name = :name,
                    trust_flag = :trust,
                    notes = :notes,
                    updated_at = now()
                WHERE id = :gid
            """), {
                'name': name or None,
                'trust': trust_flag,
                'notes': notes or None,
                'gid': guest_id,
            })

            _audit_log(conn, guest_id, 'GUEST_UPDATED',
                       json.dumps(changes), admin_id)
            conn.commit()
            flash(f'Updated {len(changes)} field(s).', 'success')
        else:
            flash('No changes detected.', 'info')

    return redirect(url_for('guests.guest_detail', guest_id=guest_id))
