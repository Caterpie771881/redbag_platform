from flask import Blueprint
from flask import request, render_template
from models.database import Setting, User, Admin
from utils.auth import admin_required


admin_manage = Blueprint("admin_manage", __name__)


@admin_manage.get("/edit_enter_password")
@admin_required
def edit_enter_password():
    """编辑入场口令接口"""
    new_enter_password = request.args.get("new")
    if new_enter_password:
        Setting.set_("enter_password", new_enter_password)
    return "ok"


@admin_manage.get("/users")
@admin_required
def show_users():
    """用户管理页面"""
    return render_template(
        "admin/users.jinja",
        users=User.select(),
        admins=Admin.select()
    )


@admin_manage.post("/edit_user")
@admin_required
def edit_user():
    """编辑用户信息"""


@admin_manage.post("/del_user")
@admin_required
def del_user():
    """删除普通用户"""


@admin_manage.post("/add_admin")
@admin_required
def add_admin():
    """添加新的管理员账户"""


@admin_manage.post("/edit_admin")
@admin_required
def edit_admin():
    """编辑管理员信息"""


@admin_manage.post("del_admin")
@admin_required
def del_admin():
    """删除管理员账户"""

