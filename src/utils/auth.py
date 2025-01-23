from flask import session, abort
from functools import wraps


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return abort(404)
        return func(*args, **kwargs)
    return wrapper
