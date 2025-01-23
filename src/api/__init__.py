from flask import Blueprint

api = Blueprint("api", __name__)

from api.v1.user import user
from api.v1.admin import admin

api.register_blueprint(user)
api.register_blueprint(admin)

