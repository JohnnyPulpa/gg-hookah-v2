"""
GG HOOKAH v2 — Admin Panel
Port: 5002
"""

import os
from datetime import timedelta
from flask import Flask, jsonify, render_template, session
from flask_cors import CORS
from sqlalchemy import create_engine, text

# --- Config ---
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://gg_hookah:password@localhost/gg_hookah"
)
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# --- App ---
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=24)
CORS(app)
# --- Prefix middleware (Flask lives behind /admin/ in Nginx) ---
class PrefixMiddleware:
    """Make url_for() generate /admin/... paths."""
    def __init__(self, wsgi_app, prefix='/admin'):
        self.wsgi_app = wsgi_app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.prefix
        return self.wsgi_app(environ, start_response)


app.wsgi_app = PrefixMiddleware(app.wsgi_app)

# --- Register auth blueprint ---
from admin.auth import auth_bp, login_required
app.register_blueprint(auth_bp)
from admin.routes.orders import orders_bp
app.register_blueprint(orders_bp)
from admin.routes.sessions import sessions_bp
app.register_blueprint(sessions_bp)
from admin.routes.menu import menu_bp
app.register_blueprint(menu_bp)
from admin.routes.dashboard import dashboard_bp
app.register_blueprint(dashboard_bp)


# --- Public routes ---

@app.route("/health")
def health():
    """Health check — no auth required."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return jsonify({
        "service": "gg-hookah-admin",
        "status": "ok" if db_status == "ok" else "degraded",
        "db": db_status
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)