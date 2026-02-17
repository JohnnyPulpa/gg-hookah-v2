"""
Admin authentication module.
Flow: Bot generates signed token → admin clicks link → session cookie set.
Only telegram_ids from ADMIN_IDS are allowed.
"""

import os
import functools
from flask import (
    Blueprint, request, redirect, url_for,
    session, jsonify, render_template, flash
)
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Load config
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me')
ADMIN_IDS = [
    int(x.strip())
    for x in os.environ.get('ADMIN_IDS', '').split(',')
    if x.strip()
]

serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_login_token(telegram_id: int) -> str:
    """Generate a signed token for admin login. Used by bot."""
    return serializer.dumps({'tid': telegram_id}, salt='admin-login')


def verify_login_token(token: str, max_age: int = 300) -> dict | None:
    """Verify token. Returns payload or None. max_age=300 = 5 minutes."""
    try:
        data = serializer.loads(token, salt='admin-login', max_age=max_age)
        return data
    except (BadSignature, SignatureExpired):
        return None


def login_required(f):
    """Decorator: redirect to login page if not authenticated."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated


def is_admin(telegram_id: int) -> bool:
    """Check if telegram_id is in ADMIN_IDS allowlist."""
    return telegram_id in ADMIN_IDS


# --- Routes ---

@auth_bp.route('/login')
def login_page():
    """Handle login: if token in query → validate → set session.
    Otherwise show 'use bot to login' page."""
    token = request.args.get('token')

    if token:
        data = verify_login_token(token)
        if data and is_admin(data.get('tid', 0)):
            session.permanent = True
            session['admin_id'] = data['tid']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid or expired link. Request a new one from the bot.'), 403

    # No token — show login instructions
    return render_template('login.html', error=None)


@auth_bp.route('/logout')
def logout():
    """Clear session and redirect to login."""
    session.clear()
    return redirect(url_for('auth.login_page'))