from functools import wraps
from flask_login import current_user
from flask import render_template
from application.models import User, Staff, Admin

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, Admin):
            return f(*args, **kwargs)
        if not isinstance(current_user, Staff):
            return render_template("error.html"), 403
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, Admin):
            return f(*args, **kwargs)
        if not isinstance(current_user, User):
            return render_template("error.html"), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not isinstance(current_user, Admin):
            return render_template("error.html"), 403
        return f(*args, **kwargs)
    return decorated_function