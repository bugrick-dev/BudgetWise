from functools import wraps
from flask import g, request, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def usd(value, type):
    """Format value as USD."""

    if type == "expense":
        return f"-${value:,.2f}"

    return f"${value:,.2f}"