"""
GG HOOKAH v2 — Backend API (Mini App)
Port: 5001
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://gg_hookah:Benxow-ziqpir-1duqbi@localhost/gg_hookah",
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")


@app.route("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return jsonify({
        "service": "gg-hookah-api",
        "status": "ok" if db_status == "ok" else "degraded",
        "db": db_status,
    })


@app.route("/")
def index():
    return jsonify({"service": "gg-hookah-api", "version": "2.0"})


@app.route("/api/mixes")
def get_mixes():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, flavors, description,
                       strength, coolness, sweetness, smokiness,
                       details, image_url, is_active, is_featured
                FROM mixes
                WHERE is_active = true
                ORDER BY sort_order, name
            """))
            mixes = []
            for row in result:
                mixes.append({
                    "id": str(row[0]),
                    "name": row[1],
                    "flavors": row[2],
                    "description": row[3],
                    "characteristics": {
                        "strength": row[4],
                        "coolness": row[5],
                        "sweetness": row[6],
                        "smokiness": row[7],
                    },
                    "details": row[8],
                    "image_url": row[9] or "",
                    "is_active": row[10],
                    "is_featured": row[11],
                    "price": 70,
                })
            return jsonify(mixes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/mixes/featured")
def get_featured_mix():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, flavors, description,
                       strength, coolness, sweetness, smokiness,
                       details, image_url, is_active, is_featured
                FROM mixes
                WHERE is_active = true AND is_featured = true
                LIMIT 1
            """))
            row = result.fetchone()
            if not row:
                return jsonify(None)
            mix = {
                "id": str(row[0]),
                "name": row[1],
                "flavors": row[2],
                "description": row[3],
                "characteristics": {
                    "strength": row[4],
                    "coolness": row[5],
                    "sweetness": row[6],
                    "smokiness": row[7],
                },
                "details": row[8],
                "image_url": row[9] or "",
                "is_active": row[10],
                "is_featured": row[11],
                "price": 70,
            }
            return jsonify(mix)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/drinks")
def get_drinks():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, price_gel, image_url, is_active
                FROM menu_items
                WHERE item_type = 'drink' AND is_active = true
                ORDER BY sort_order, name
            """))
            drinks = []
            for row in result:
                drinks.append({
                    "id": str(row[0]),
                    "name": row[1],
                    "price": row[2],
                    "image_url": row[3] or "",
                    "is_active": row[4],
                })
            return jsonify(drinks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)


# ─── POST /api/orders ─────────────────────────────────────────
from flask import request
from datetime import datetime, time as dtime
import pytz

TBILISI_TZ = pytz.timezone("Asia/Tbilisi")

# Allowed statuses that mean "order is active"
ACTIVE_STATUSES = (
    "NEW", "CONFIRMED", "ON_THE_WAY", "DELIVERED",
    "SESSION_ACTIVE", "SESSION_ENDING", "WAITING_FOR_PICKUP",
)


def _get_setting(conn, key, default=None):
    """Read a single setting from the settings table."""
    row = conn.execute(
        text("SELECT value FROM settings WHERE key = :k"),
        {"k": key},
    ).fetchone()
    return row[0] if row else default


@app.route("/api/orders", methods=["POST"])
def create_order():
    """
    Create a new order (Spec Section 3.1).
    Expects JSON body with: telegram_id, mix_id, drinks, address_text,
    entrance, floor, apartment, door_code, phone, comment, deposit_type,
    promo_code.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400

        # --- Required fields ---
        telegram_id = data.get("telegram_id")
        mix_id = data.get("mix_id")
        address_text = data.get("address_text", "").strip()
        phone = data.get("phone", "").strip()

        if not telegram_id or not mix_id or not address_text or not phone:
            return jsonify({"error": "Missing required fields: telegram_id, mix_id, address_text, phone"}), 400

        # --- Optional fields ---
        drinks = data.get("drinks", [])  # [{drink_id, qty}]
        entrance = data.get("entrance", "")
        floor_val = data.get("floor", "")
        apartment = data.get("apartment", "")
        door_code = data.get("door_code", "")
        comment = data.get("comment", "")
        deposit_type = data.get("deposit_type", "cash")
        promo_code_input = data.get("promo_code", "").strip().upper()

        if deposit_type not in ("cash", "passport"):
            deposit_type = "cash"

        with engine.begin() as conn:
            # --- 1. Read settings ---
            base_bowl_price = int(_get_setting(conn, "base_bowl_price", "70"))
            drinks_max_qty = int(_get_setting(conn, "drinks_max_total_qty", "8"))
            deposit_amount = int(_get_setting(conn, "deposit_amount", "100"))
            late_cutoff = _get_setting(conn, "late_order_cutoff_time", "01:30")

            # --- 2. Validate mix exists and active ---
            mix_row = conn.execute(
                text("SELECT id, name FROM mixes WHERE id = :mid AND is_active = true"),
                {"mid": mix_id},
            ).fetchone()
            if not mix_row:
                return jsonify({"error": "Mix not found or inactive"}), 400

            # --- 3. Validate drinks ---
            total_drink_qty = 0
            validated_drinks = []
            for d in drinks:
                drink_id = d.get("drink_id")
                qty = int(d.get("qty", 0))
                if qty <= 0:
                    continue
                total_drink_qty += qty
                drink_row = conn.execute(
                    text("SELECT id, name, price_gel FROM menu_items WHERE id = :did AND item_type = 'drink' AND is_active = true"),
                    {"did": drink_id},
                ).fetchone()
                if not drink_row:
                    return jsonify({"error": f"Drink not found: {drink_id}"}), 400
                validated_drinks.append({
                    "id": str(drink_row[0]),
                    "name": drink_row[1],
                    "price": drink_row[2],
                    "qty": qty,
                })

            if total_drink_qty > drinks_max_qty:
                return jsonify({"error": f"Max {drinks_max_qty} drinks per order"}), 400

            # --- 4. Check no active order for this telegram_id ---
            active = conn.execute(
                text("SELECT id FROM orders WHERE telegram_id = :tid AND status IN :sts LIMIT 1"),
                {"tid": telegram_id, "sts": tuple(ACTIVE_STATUSES)},
            ).fetchone()
            if active:
                return jsonify({"error": "You already have an active order", "active_order_id": str(active[0])}), 409

            # --- 5. Find or create guest by phone ---
            guest_row = conn.execute(
                text("SELECT id, passport_photo_url FROM guests WHERE phone = :ph"),
                {"ph": phone},
            ).fetchone()
            if guest_row:
                guest_id = str(guest_row[0])
                has_passport = guest_row[1] is not None
            else:
                result = conn.execute(
                    text("INSERT INTO guests (phone, telegram_id) VALUES (:ph, :tid) RETURNING id"),
                    {"ph": phone, "tid": telegram_id},
                )
                guest_id = str(result.fetchone()[0])
                has_passport = False

            # If passport on file, deposit not needed
            if has_passport:
                deposit_type = "none"

            # --- 6. Check late order ---
            now_tbilisi = datetime.now(TBILISI_TZ)
            cutoff_parts = late_cutoff.split(":")
            cutoff_time = dtime(int(cutoff_parts[0]), int(cutoff_parts[1]))
            is_late = now_tbilisi.time() > cutoff_time and now_tbilisi.time() < dtime(5, 0)

            # --- 7. Validate promo code (if provided) ---
            promo_percent = 0
            promo_code_record_id = None
            if promo_code_input:
                promo_row = conn.execute(
                    text("""
                        SELECT id, percent, max_uses, used_count
                        FROM promo_codes
                        WHERE code = :code AND is_active = true
                          AND valid_from <= now() AND valid_until > now()
                    """),
                    {"code": promo_code_input},
                ).fetchone()
                if not promo_row:
                    return jsonify({"error": "Invalid or expired promo code"}), 400
                if promo_row[3] >= promo_row[2]:
                    return jsonify({"error": "Promo code usage limit reached"}), 400
                # Check per-phone usage
                already_used = conn.execute(
                    text("SELECT id FROM promo_code_usages WHERE promo_code_id = :pid AND phone = :ph"),
                    {"pid": str(promo_row[0]), "ph": phone},
                ).fetchone()
                if already_used:
                    return jsonify({"error": "Promo code already used by this phone"}), 400
                promo_percent = promo_row[1]
                promo_code_record_id = str(promo_row[0])

            # --- 8. Check personal discount ---
            discount_percent = 0
            discount_id = None
            discount_row = conn.execute(
                text("""
                    SELECT id, percent FROM discounts
                    WHERE phone = :ph AND is_used = false AND valid_until > now()
                    LIMIT 1
                """),
                {"ph": phone},
            ).fetchone()
            if discount_row:
                discount_percent = discount_row[1]
                discount_id = str(discount_row[0])

            # --- 9. Calculate pricing ---
            # Best discount wins (promo or personal, not both)
            applied_percent = max(promo_percent, discount_percent)
            if promo_percent >= discount_percent:
                final_promo_percent = promo_percent
                final_discount_percent = 0
                final_discount_id = None
            else:
                final_promo_percent = 0
                final_discount_percent = discount_percent
                final_discount_id = discount_id
                promo_code_input = ""
                promo_code_record_id = None

            hookah_discounted = base_bowl_price - int(base_bowl_price * applied_percent / 100)
            drinks_total = sum(d["price"] * d["qty"] for d in validated_drinks)

            # --- 10. Insert order ---
            order_result = conn.execute(
                text("""
                    INSERT INTO orders (
                        telegram_id, phone, guest_id, mix_id,
                        address_text, entrance, floor, apartment, door_code,
                        comment, deposit_type, deposit_amount_gel,
                        promo_code, promo_percent, discount_percent, discount_id,
                        is_late_order, status
                    ) VALUES (
                        :tid, :phone, :gid, :mid,
                        :addr, :ent, :fl, :apt, :dc,
                        :cmt, :dep_type, :dep_amt,
                        :promo, :promo_pct, :disc_pct, :disc_id,
                        :late, 'NEW'
                    ) RETURNING id, created_at
                """),
                {
                    "tid": telegram_id, "phone": phone, "gid": guest_id, "mid": mix_id,
                    "addr": address_text, "ent": entrance, "fl": floor_val, "apt": apartment, "dc": door_code,
                    "cmt": comment, "dep_type": deposit_type, "dep_amt": deposit_amount,
                    "promo": promo_code_input or None, "promo_pct": final_promo_percent or None,
                    "disc_pct": final_discount_percent or None, "disc_id": final_discount_id,
                    "late": is_late,
                },
            )
            order_row = order_result.fetchone()
            order_id = str(order_row[0])

            # --- 11. Insert order_items: hookah ---
            conn.execute(
                text("""
                    INSERT INTO order_items (order_id, item_type, mix_id, quantity, unit_price_gel, total_price_gel)
                    VALUES (:oid, 'hookah', :mid, 1, :price, :total)
                """),
                {"oid": order_id, "mid": mix_id, "price": base_bowl_price, "total": hookah_discounted},
            )

            # --- 12. Insert order_items: drinks ---
            for d in validated_drinks:
                conn.execute(
                    text("""
                        INSERT INTO order_items (order_id, item_type, menu_item_id, quantity, unit_price_gel, total_price_gel)
                        VALUES (:oid, 'drink', :did, :qty, :price, :total)
                    """),
                    {"oid": order_id, "did": d["id"], "qty": d["qty"], "price": d["price"], "total": d["price"] * d["qty"]},
                )

            # --- 13. Mark discount as used (if applied) ---
            if final_discount_id:
                conn.execute(
                    text("UPDATE discounts SET is_used = true, used_at = now(), used_order_id = :oid WHERE id = :did"),
                    {"oid": order_id, "did": final_discount_id},
                )

            # --- 14. Record promo usage + increment used_count ---
            if promo_code_record_id:
                conn.execute(
                    text("INSERT INTO promo_code_usages (promo_code_id, phone, order_id) VALUES (:pid, :ph, :oid)"),
                    {"pid": promo_code_record_id, "ph": phone, "oid": order_id},
                )
                conn.execute(
                    text("UPDATE promo_codes SET used_count = used_count + 1 WHERE id = :pid"),
                    {"pid": promo_code_record_id},
                )

            # --- 15. Increment guest total_orders ---
            conn.execute(
                text("UPDATE guests SET total_orders = total_orders + 1, updated_at = now() WHERE id = :gid"),
                {"gid": guest_id},
            )

            return jsonify({
                "order_id": order_id,
                "status": "NEW",
                "hookah_price": hookah_discounted,
                "drinks_total": drinks_total,
                "total": hookah_discounted + drinks_total,
                "discount_applied": applied_percent,
                "is_late_order": is_late,
            }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
# This will be appended to app.py

# ─── GET /api/orders ──────────────────────────────────────────

@app.route("/api/orders", methods=["GET"])
def get_orders():
    """
    Get orders for a telegram user.
    Query params: telegram_id (required)
    Returns: { active: order|null, history: [orders] }
    """
    try:
        telegram_id = request.args.get("telegram_id")
        if not telegram_id:
            return jsonify({"error": "telegram_id is required"}), 400

        with engine.connect() as conn:
            rows = conn.execute(
                text("""
                    SELECT o.id, o.status, o.phone, o.address_text,
                           o.hookah_count, o.deposit_type,
                           o.promised_time, o.promised_eta_text,
                           o.session_started_at, o.session_ends_at,
                           o.free_extension_used, o.is_late_order,
                           o.created_at, o.completed_at, o.canceled_at,
                           o.promo_code, o.promo_percent, o.discount_percent,
                           m.name as mix_name, m.flavors as mix_flavors,
                           m.image_url as mix_image
                    FROM orders o
                    JOIN mixes m ON m.id = o.mix_id
                    WHERE o.telegram_id = :tid
                    ORDER BY o.created_at DESC
                """),
                {"tid": int(telegram_id)},
            ).fetchall()

            active = None
            history = []

            for r in rows:
                order_data = {
                    "id": str(r[0]),
                    "status": r[1],
                    "phone": r[2],
                    "address": r[3],
                    "hookah_count": r[4],
                    "deposit_type": r[5],
                    "promised_time": r[6].isoformat() if r[6] else None,
                    "promised_eta_text": r[7],
                    "session_started_at": r[8].isoformat() if r[8] else None,
                    "session_ends_at": r[9].isoformat() if r[9] else None,
                    "free_extension_used": r[10],
                    "is_late_order": r[11],
                    "created_at": r[12].isoformat() if r[12] else None,
                    "completed_at": r[13].isoformat() if r[13] else None,
                    "canceled_at": r[14].isoformat() if r[14] else None,
                    "promo_code": r[15],
                    "promo_percent": r[16],
                    "discount_percent": r[17],
                    "mix_name": r[18],
                    "mix_flavors": r[19],
                    "mix_image": r[20] or "",
                }

                items = conn.execute(
                    text("""
                        SELECT oi.item_type, oi.quantity,
                               oi.unit_price_gel, oi.total_price_gel,
                               m.name as mix_name, mi.name as drink_name
                        FROM order_items oi
                        LEFT JOIN mixes m ON m.id = oi.mix_id
                        LEFT JOIN menu_items mi ON mi.id = oi.menu_item_id
                        WHERE oi.order_id = :oid
                    """),
                    {"oid": str(r[0])},
                ).fetchall()

                order_items = []
                total = 0
                for item in items:
                    order_items.append({
                        "type": item[0],
                        "quantity": item[1],
                        "unit_price": item[2],
                        "total_price": item[3],
                        "name": item[4] or item[5],
                    })
                    total += item[3]

                order_data["items"] = order_items
                order_data["total"] = total

                if r[1] in ACTIVE_STATUSES and active is None:
                    active = order_data
                else:
                    history.append(order_data)

            return jsonify({"active": active, "history": history})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500