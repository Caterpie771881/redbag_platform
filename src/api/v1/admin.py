from flask import Blueprint
from flask import (
    session,
    request,
    render_template,
    redirect,
)
from flask import current_app as app
from models.forms import (
    LoginForm,
    TopicCreateForm,
    RedbagCreateForm,
    TopicDeleteForm,
    RedbagDeleteForm,
    RedbagUpdateForm,
)
from models.database import (
    Admin,
    Topic,
    Redbag,
)
from utils.auth import admin_required
from peewee import IntegrityError


admin = Blueprint("admin", __name__, url_prefix="/admin")


def render_dashboard(
        msg={},
        topic_create_form=None,
        topic_update_form=None,
        redbag_create_form=None,
        redbag_update_form=None,
    ):
    """渲染管理员面板"""
    if not topic_create_form:
        topic_create_form = TopicCreateForm()
    if not redbag_create_form:
        redbag_create_form = RedbagCreateForm()
    if not redbag_update_form:
        redbag_update_form = RedbagUpdateForm()
    
    def make_redbag_update_form(redbag: Redbag):
        return render_template(
            "admin/redbag_update.jinja",
            form=redbag_create_form,
            redbag=redbag
        )
    
    return render_template(
        "admin/dashboard.jinja",
        topic_create_form=render_template(
            "admin/topic_create.jinja",
            form=topic_create_form,
            error=msg.get("topic_form_error")
        ),
        redbag_create_form=render_template(
            "admin/redbag_create.jinja",
            form=redbag_create_form,
            error=msg.get("redbag_form_error")
        ),
        redbag_update_form=make_redbag_update_form,
        topics=Topic.select(),
        redbags=Redbag.select()
    )


@admin.route("/")
@admin_required
def index():
    return render_dashboard()


@admin.get("/login")
def show_login_form():
    """登录接口"""
    return render_template("admin/login.jinja", form=LoginForm())


@admin.post("/login")
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


@admin.post("/create_topic")
@admin_required
def create_topic():
    """创建题目"""
    form = TopicCreateForm()
    if not form.validate_on_submit():
        return render_dashboard(
            {"topic_form_error": "非法输入, 请检查"},
            topic_create_form=form,
        )
    try:
        new_topic: Topic = Topic.create_topic(
            name=form.name.data,
            type=form.type.data,
            redbag=form.redbag.data,
            flag=form.flag.data
        )
        new_topic.save()
    except IntegrityError:
        return render_dashboard(
            {"topic_form_error": "重复的 Flag"},
            topic_create_form=form,
        )
    return render_dashboard()


@admin.post("/create_redbag")
@admin_required
def create_redbag():
    """创建红包"""
    form = RedbagCreateForm()
    if not form.validate_on_submit():
        return render_dashboard(
            {"redbag_form_error": "非法输入, 请检查"},
            redbag_create_form=form,
        )
    try:
        Redbag.insert(
            name=form.name.data,
            password=form.password.data,
        ).execute()
    except IntegrityError:
        return render_dashboard(
            {"redbag_form_error": "重复的红包口令"},
            redbag_create_form=form,
        )
    return render_dashboard()


@admin.post("/del_topic")
@admin_required
def del_topic():
    """删除题目"""
    form = TopicDeleteForm()
    if not form.validate_on_submit():
        return render_dashboard()
    topic_to_del: Topic = Topic.get_or_none(
        Topic.id == form.topic_id.data
    )
    if not topic_to_del:
        return "你要干嘛?"
    try:
        topic_to_del.delete_instance()
    except:
        return "删除失败"
    return render_dashboard()


@admin.post("/del_redbag")
@admin_required
def del_redbag():
    """删除红包"""
    form = RedbagDeleteForm()
    if not form.validate_on_submit():
        return render_dashboard()
    redbag_to_del: Redbag = Redbag.get_or_none(
        Redbag.id == form.redbag_id.data
    )
    if not redbag_to_del:
        return "你要干嘛?"
    try:
        topics_need_redbag = (Topic
                              .select()
                              .where(Topic.redbag == redbag_to_del))
        for topic in topics_need_redbag:
            topic.delete_instance()
        redbag_to_del.delete_instance()
    except:
        return "删除失败, 你可能需要先把对应该红包的题目删除"
    return render_dashboard()


@admin.post("/update_redbag")
@admin_required
def update_redbag():
    """更新红包"""
    form = RedbagUpdateForm()
    if not form.validate_on_submit():
        return render_dashboard()
    redbag_to_update: Redbag = Redbag.get_or_none(
        Redbag.id == form.redbag_id.data
    )
    if not redbag_to_update:
        return "不存在该红包"
    try:
        if form.name.data:
            redbag_to_update.name = form.name.data
        if form.password.data:
            redbag_to_update.password = form.password.data
        redbag_to_update.save()
    except:
        return "发生错误, 修改失败"
    return render_dashboard()

