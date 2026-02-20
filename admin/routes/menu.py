"""
Admin Menu routes.
Spec 6.10: Mixes + Drinks CRUD.
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from sqlalchemy import text
from admin.auth import login_required

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')


def _audit_log(conn, entity_type, entity_id, action, details, admin_id):
    """Insert audit log entry."""
    conn.execute(text("""
        INSERT INTO audit_logs (entity_type, entity_id, action, details, admin_telegram_id)
        VALUES (:etype, :eid, :action, :details, :admin_id)
    """), {
        'etype': entity_type,
        'eid': str(entity_id),
        'action': action,
        'details': details,
        'admin_id': admin_id,
    })


# ==================== MIXES ====================

@menu_bp.route('/')
@login_required
def menu_index():
    """Menu overview — redirect to mixes."""
    return redirect(url_for('menu.mixes_list'))


@menu_bp.route('/mixes/')
@login_required
def mixes_list():
    """List all mixes."""
    from admin.app import engine

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT * FROM mixes ORDER BY sort_order ASC, created_at DESC
        """)).mappings().all()

    mixes = [dict(r) for r in rows]
    for m in mixes:
        m['id_short'] = str(m['id'])[:8]

    return render_template('menu_mixes.html', mixes=mixes)


@menu_bp.route('/mixes/new', methods=['GET', 'POST'])
@login_required
def mix_create():
    """Create a new mix."""
    from admin.app import engine

    if request.method == 'POST':
        return _save_mix(engine, mix_id=None)

    return render_template('menu_mix_form.html', mix=None, is_edit=False)


@menu_bp.route('/mixes/<mix_id>/edit', methods=['GET', 'POST'])
@login_required
def mix_edit(mix_id):
    """Edit existing mix."""
    from admin.app import engine

    if request.method == 'POST':
        return _save_mix(engine, mix_id=mix_id)

    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM mixes WHERE id = :mid"),
                           {'mid': mix_id}).mappings().first()
        if not row:
            return "Mix not found", 404

    return render_template('menu_mix_form.html', mix=dict(row), is_edit=True)


def _save_mix(engine, mix_id=None):
    """Create or update a mix from form data."""
    admin_id = session.get('admin_id')

    name = request.form.get('name', '').strip()
    flavors = request.form.get('flavors', '').strip()
    description = request.form.get('description', '').strip() or None
    details = request.form.get('details', '').strip() or None
    image_url = request.form.get('image_url', '').strip()
    strength = request.form.get('strength', 3, type=int)
    coolness = request.form.get('coolness', 3, type=int)
    sweetness = request.form.get('sweetness', 3, type=int)
    smokiness = request.form.get('smokiness', 3, type=int)
    is_active = request.form.get('is_active') == 'on'
    is_featured = request.form.get('is_featured') == 'on'
    sort_order = request.form.get('sort_order', 0, type=int)

    # Validate
    if not name or not flavors or not image_url:
        return "Name, flavors, and image_url are required", 400

    # Clamp characteristics 1-5
    strength = max(1, min(5, strength))
    coolness = max(1, min(5, coolness))
    sweetness = max(1, min(5, sweetness))
    smokiness = max(1, min(5, smokiness))

    with engine.connect() as conn:
        # If setting as featured, unset any other featured mix
        if is_featured:
            if mix_id:
                conn.execute(text("""
                    UPDATE mixes SET is_featured = false, updated_at = now()
                    WHERE is_featured = true AND id != :mid
                """), {'mid': mix_id})
            else:
                conn.execute(text("""
                    UPDATE mixes SET is_featured = false, updated_at = now()
                    WHERE is_featured = true
                """))

        if mix_id:
            # UPDATE
            conn.execute(text("""
                UPDATE mixes SET
                    name = :name, flavors = :flavors, description = :desc,
                    details = :details, image_url = :img,
                    strength = :str, coolness = :cool, sweetness = :sweet, smokiness = :smoke,
                    is_active = :active, is_featured = :featured, sort_order = :sort,
                    updated_at = now()
                WHERE id = :mid
            """), {
                'mid': mix_id, 'name': name, 'flavors': flavors, 'desc': description,
                'details': details, 'img': image_url,
                'str': strength, 'cool': coolness, 'sweet': sweetness, 'smoke': smokiness,
                'active': is_active, 'featured': is_featured, 'sort': sort_order,
            })
            _audit_log(conn, 'mix', mix_id, 'MIX_UPDATED',
                       f'{{"name":"{name}"}}', admin_id)
        else:
            # INSERT
            result = conn.execute(text("""
                INSERT INTO mixes (name, flavors, description, details, image_url,
                    strength, coolness, sweetness, smokiness,
                    is_active, is_featured, sort_order)
                VALUES (:name, :flavors, :desc, :details, :img,
                    :str, :cool, :sweet, :smoke,
                    :active, :featured, :sort)
                RETURNING id
            """), {
                'name': name, 'flavors': flavors, 'desc': description,
                'details': details, 'img': image_url,
                'str': strength, 'cool': coolness, 'sweet': sweetness, 'smoke': smokiness,
                'active': is_active, 'featured': is_featured, 'sort': sort_order,
            })
            new_id = result.fetchone()[0]
            _audit_log(conn, 'mix', str(new_id), 'MIX_CREATED',
                       f'{{"name":"{name}"}}', admin_id)

        conn.commit()

    return redirect(url_for('menu.mixes_list'))


@menu_bp.route('/mixes/<mix_id>/toggle', methods=['POST'])
@login_required
def mix_toggle_active(mix_id):
    """Quick toggle is_active for a mix."""
    from admin.app import engine
    admin_id = session.get('admin_id')

    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE mixes SET is_active = NOT is_active, updated_at = now()
            WHERE id = :mid
        """), {'mid': mix_id})
        _audit_log(conn, 'mix', mix_id, 'MIX_TOGGLED', '{}', admin_id)
        conn.commit()

    return redirect(url_for('menu.mixes_list'))


@menu_bp.route('/mixes/<mix_id>/feature', methods=['POST'])
@login_required
def mix_set_featured(mix_id):
    """Set this mix as featured (unset others)."""
    from admin.app import engine
    admin_id = session.get('admin_id')

    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE mixes SET is_featured = false, updated_at = now()
            WHERE is_featured = true
        """))
        conn.execute(text("""
            UPDATE mixes SET is_featured = true, updated_at = now()
            WHERE id = :mid
        """), {'mid': mix_id})
        _audit_log(conn, 'mix', mix_id, 'MIX_SET_FEATURED', '{}', admin_id)
        conn.commit()

    return redirect(url_for('menu.mixes_list'))


# ==================== DRINKS ====================

@menu_bp.route('/drinks/')
@login_required
def drinks_list():
    """List all drinks."""
    from admin.app import engine

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT * FROM menu_items
            WHERE item_type = 'drink'
            ORDER BY sort_order ASC, created_at DESC
        """)).mappings().all()

    drinks = [dict(r) for r in rows]
    for d in drinks:
        d['id_short'] = str(d['id'])[:8]

    return render_template('menu_drinks.html', drinks=drinks)


@menu_bp.route('/drinks/new', methods=['GET', 'POST'])
@login_required
def drink_create():
    """Create a new drink."""
    from admin.app import engine

    if request.method == 'POST':
        return _save_drink(engine, drink_id=None)

    return render_template('menu_drink_form.html', drink=None, is_edit=False)


@menu_bp.route('/drinks/<drink_id>/edit', methods=['GET', 'POST'])
@login_required
def drink_edit(drink_id):
    """Edit existing drink."""
    from admin.app import engine

    if request.method == 'POST':
        return _save_drink(engine, drink_id=drink_id)

    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM menu_items WHERE id = :did"),
                           {'did': drink_id}).mappings().first()
        if not row:
            return "Drink not found", 404

    return render_template('menu_drink_form.html', drink=dict(row), is_edit=True)


def _save_drink(engine, drink_id=None):
    """Create or update a drink from form data."""
    admin_id = session.get('admin_id')

    name = request.form.get('name', '').strip()
    price_gel = request.form.get('price_gel', 0, type=int)
    image_url = request.form.get('image_url', '').strip() or None
    is_active = request.form.get('is_active') == 'on'
    sort_order = request.form.get('sort_order', 0, type=int)

    if not name or price_gel <= 0:
        return "Name and price are required", 400

    with engine.connect() as conn:
        if drink_id:
            conn.execute(text("""
                UPDATE menu_items SET
                    name = :name, price_gel = :price, image_url = :img,
                    is_active = :active, sort_order = :sort, updated_at = now()
                WHERE id = :did
            """), {
                'did': drink_id, 'name': name, 'price': price_gel,
                'img': image_url, 'active': is_active, 'sort': sort_order,
            })
            _audit_log(conn, 'drink', drink_id, 'DRINK_UPDATED',
                       f'{{"name":"{name}"}}', admin_id)
        else:
            result = conn.execute(text("""
                INSERT INTO menu_items (item_type, name, price_gel, image_url, is_active, sort_order)
                VALUES ('drink', :name, :price, :img, :active, :sort)
                RETURNING id
            """), {
                'name': name, 'price': price_gel,
                'img': image_url, 'active': is_active, 'sort': sort_order,
            })
            new_id = result.fetchone()[0]
            _audit_log(conn, 'drink', str(new_id), 'DRINK_CREATED',
                       f'{{"name":"{name}"}}', admin_id)

        conn.commit()

    return redirect(url_for('menu.drinks_list'))


@menu_bp.route('/drinks/<drink_id>/toggle', methods=['POST'])
@login_required
def drink_toggle_active(drink_id):
    """Quick toggle is_active for a drink."""
    from admin.app import engine
    admin_id = session.get('admin_id')

    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE menu_items SET is_active = NOT is_active, updated_at = now()
            WHERE id = :did
        """), {'did': drink_id})
        _audit_log(conn, 'drink', drink_id, 'DRINK_TOGGLED', '{}', admin_id)
        conn.commit()

    return redirect(url_for('menu.drinks_list'))