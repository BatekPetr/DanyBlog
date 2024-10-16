from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin is False:
            flash("You are not permitted to view this page.", "warning")
            return redirect(url_for("core.index"))
        return func(*args, **kwargs)

    return decorated_function


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already authenticated.", "info")
            return redirect(url_for("core.index"))
        return func(*args, **kwargs)

    return decorated_function


def check_is_approved(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_approved is False:
            flash("Your access has not been approved yet.", "warning")
            return redirect(url_for("accounts.inactive"))
        return func(*args, **kwargs)

    return decorated_function