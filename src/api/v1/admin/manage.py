from flask import Blueprint
from flask import request, render_template, flash
from models.database import (
    Setting,
    User,
    Admin,
    Solve,
)
from models.forms import AddAdminForm, EditAdminForm
from utils.auth import admin_required
from utils.crypto import md5


admin_manage = Blueprint("admin_manage", __name__)


def render_user_manage_page():
    """渲染用户管理页面"""
    return render_template(
        "admin/users.jinja",
        add_admin_form=AddAdminForm(),
        edit_admin_form=EditAdminForm(),
        users=User.select(),
        admins=Admin.select(),
    )


def render_setting_manage_page():
    """渲染设置管理页面"""
    return render_template(
        "admin/settings.jinja",
        enter_password=Setting.get_("enter_password"),
    )


@admin_manage.get("/edit_enter_password")
@admin_required
def edit_enter_password():
    """编辑入场口令接口"""
    new_enter_password = request.args.get("new")
    if new_enter_password:
        Setting.set_("enter_password", new_enter_password)
        flash("修改成功", "success")
    return render_setting_manage_page()


@admin_manage.get("/users")
@admin_required
def show_users():
    """用户管理页面"""
    return render_user_manage_page()


@admin_manage.get("/ban_user")
@admin_required
def ban_user():
    """封禁普通用户"""
    user_id = request.args.get("id")
    user_to_ban: User = User.get_or_none(User.id == user_id)
    if user_to_ban:
        user_to_ban.ban = True
        user_to_ban.save()
    return render_user_manage_page()


@admin_manage.get("/allow_user")
@admin_required
def allow_user():
    """解封普通用户"""
    user_id = request.args.get("id")
    user_to_allow: User = User.get_or_none(User.id == user_id)
    if user_to_allow:
        user_to_allow.ban = False
        user_to_allow.save()
    return render_user_manage_page()


@admin_manage.get("/del_user")
@admin_required
def del_user():
    """删除普通用户"""
    user_id = request.args.get("id")
    user_to_del: User = User.get_or_none(User.id == user_id)
    if not user_to_del:
        flash("用户不存在", "warning")
        return render_user_manage_page()
    
    try:
        Solve.delete().where(Solve.user == user_to_del).execute()
        user_to_del.delete_instance()
    except:
        flash("发生错误, 删除失败", "error")
        return render_user_manage_page()
    
    flash(f"已删除用户 {user_to_del.username}", "success")
    return render_user_manage_page()


@admin_manage.post("/add_admin")
@admin_required
def add_admin():
    """添加新的管理员账户"""
    form = AddAdminForm()
    if not form.validate_on_submit():
        flash("非法输入, 请检查", "error")
        return render_user_manage_page()
    
    new_admin, created = Admin.get_or_create(
        username = form.username.data,
        defaults={
            "password": md5(form.password.data)
        }
    )
    if not created:
        flash("用户名已存在", "error")
        return render_user_manage_page()
    
    flash("添加成功", "success")
    return render_user_manage_page()


@admin_manage.post("/edit_admin")
@admin_required
def edit_admin():
    """编辑管理员信息"""
    form = EditAdminForm()
    if not form.validate_on_submit():
        flash("非法输入, 请检查", "error")
        return render_user_manage_page()
    
    admin_id = form.admin_id.data
    admin_to_edit: Admin = Admin.get_or_none(Admin.id == admin_id)
    if not admin_to_edit:
        flash("用户不存在", "error")
        return render_user_manage_page()
    
    try:
        admin_to_edit.username = form.username.data
        admin_to_edit.password = md5(form.password.data)
        admin_to_edit.save()
    except:
        flash("发生错误, 修改失败", "error")
        return render_user_manage_page()
    
    flash("编辑成功", "success")
    return render_user_manage_page()


@admin_manage.get("/del_admin")
@admin_required
def del_admin():
    """删除管理员账户"""
    admin_id = request.args.get("id")

    admin_to_del: Admin = Admin.get_or_none(Admin.id == admin_id)
    if not admin_to_del:
        flash("用户不存在", "error")
        return render_user_manage_page()
    
    if Admin.select().count() <= 1:
        flash("至少需要存在一个管理员", "warning")
        return render_user_manage_page()
    
    admin_to_del.delete_instance()
    flash(f"已删除用户 {admin_to_del.username}", "success")
    return render_user_manage_page()


@admin_manage.get("/settings")
@admin_required
def show_settings():
    """设置管理页面"""
    return render_setting_manage_page()
