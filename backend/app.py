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
