import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app


def requires_login(func: Callable) -> Callable:
    # functools allows to take the name and documentation of original function
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('rks_email'):
            flash('You need to be signed in for this page.', 'danger')
            # bp_user is blue print name in users_bp.py
            return redirect(url_for('bp_users.login_user'))
        return func(*args, **kwargs)
    # Return the function and not its execution result thus do not include brackets
    return decorated_function

def requires_admin(func: Callable) -> Callable:
    # functools allows to take the name and documentation of original function
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('rks_email') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this page.', 'danger')
            # bp_user is blue print name in users_bp.py
            return redirect(url_for('bp_users.login_user'))
        return func(*args, **kwargs)
    # Return the function and not its execution result thus do not include brackets
    return decorated_function
