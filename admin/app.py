"""
GG HOOKAH v2 — Admin Panel
Port: 5002
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://gg_hookah:Benxow-ziqpir-1duqbi@localhost/gg_hookah")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
app = Flask(__name__)
CORS(app)

ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "904970735").split(",")]

@app.route("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return jsonify({"service": "gg-hookah-admin", "status": "ok" if db_status == "ok" else "degraded", "db": db_status})

@app.route("/")
def index():
    return jsonify({"service": "gg-hookah-admin", "version": "2.0"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
