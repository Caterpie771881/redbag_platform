from flask import Blueprint
from flask import (
    session,
    render_template,
    redirect,
)
from flask import current_app as app
from models.forms import LoginForm
from models.database import Admin
from utils.auth import admin_required


admin_auth = Blueprint("admin_auth", __name__)


@admin_auth.get("/login")
def show_login_form():
    """登录接口"""
    return render_template("admin/login.jinja", form=LoginForm())


@admin_auth.post("/login")
def admin_login():
    """登录接口"""
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template(
            "admin/login.jinja",
            form=form,
            error="非法输入, 请检查"
        )
    username = form.username.data
    password = form.password.data
    admin = Admin.check(username, password)
    if admin:
        session["id"] = admin.id
        return redirect("/admin")
    return render_template(
        "admin/login.jinja",
        form=form,
        error="用户名或密码错误"
    )


@admin_auth.get("/logout")
@admin_required
def logout():
    """登出接口"""
    del session["id"]
    return redirect("/admin/login")