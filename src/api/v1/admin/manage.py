from flask import Blueprint
from flask import request
from models.database import Setting
from utils.auth import admin_required


admin_manage = Blueprint("admin_manage", __name__)


@admin_manage.get("/edit_enter_password")
@admin_required
def edit_enter_password():
    """编辑入参口令接口"""
    new_enter_password = request.args.get("new")
    if new_enter_password:
        Setting.set_("enter_password", new_enter_password)
    return "ok"


@admin_manage.get("/users")
@admin_required
def show_users():
    """用户管理页面"""
    