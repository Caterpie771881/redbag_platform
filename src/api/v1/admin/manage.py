from flask import Blueprint
from flask import request, render_template, redirect
from models.database import Setting, User, Admin
from utils.auth import admin_required
from utils.message import message_set as msgs


admin_manage = Blueprint("admin_manage", __name__)


def render_manage_page():
    """渲染用户管理页面"""
    return render_template(
        "admin/users.jinja",
        users=User.select(),
        admins=Admin.select(),
    )


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
    return render_manage_page()


@admin_manage.get("/ban_user")
@admin_required
def ban_user():
    """封禁普通用户"""
    user_id = request.args.get("id")
    user_to_ban: User = User.get_or_none(User.id == user_id)
    if user_to_ban:
        user_to_ban.ban = True
        user_to_ban.save()
    return render_manage_page()


@admin_manage.get("/allow_user")
@admin_required
def allow_user():
    """解封普通用户"""
    user_id = request.args.get("id")
    user_to_allow: User = User.get_or_none(User.id == user_id)
    if user_to_allow:
        user_to_allow.ban = False
        user_to_allow.save()
    return render_manage_page()


@admin_manage.get("/del_user")
@admin_required
def del_user():
    """删除普通用户"""
    user_id = request.args.get("id")
    user_to_del: User = User.get_or_none(User.id == user_id)
    if user_to_del:
        user_to_del.delete_instance()
    return render_manage_page()


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

