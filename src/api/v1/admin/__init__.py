from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix="/admin")

from .dashboard import admin_dashboard
from .auth import admin_auth
from .manage import admin_manage

admin.register_blueprint(admin_dashboard)
admin.register_blueprint(admin_auth)
admin.register_blueprint(admin_manage)
