from flask import session, abort, sessions
from functools import wraps


def admin_required(func):
    """admin 鉴权装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return abort(404)
        return func(*args, **kwargs)
    return wrapper


def record_ip(func):
    """被装饰的视图函数会记录访问者 ip 及其操作"""
    from flask import request
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("ip:", request.remote_addr)
        return func(*args, **kwargs)
    return wrapper

