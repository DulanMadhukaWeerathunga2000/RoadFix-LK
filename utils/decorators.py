from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user
# We re-export login_required from flask_login for backward compatibility in our app
from flask_login import login_required


def roles_required(*roles):
    """Restrict a view to one or more roles, e.g. @roles_required('admin', 'officer')."""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator
