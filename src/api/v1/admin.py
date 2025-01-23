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
)
from models.database import (
    Admin,
    Topic,
    Redbag,
)
from utils.auth import admin_required
from peewee import IntegrityError


admin = Blueprint("admin", __name__, url_prefix="/admin")


def render_dashboard(msg={}, topic_form=None, redbag_form=None):

    if topic_form == None:
        topic_form = TopicCreateForm()
    if redbag_form == None:
        redbag_form = RedbagCreateForm()
    
    return render_template(
        "admin/dashboard.jinja",
        topic_form=render_template(
            "admin/topic.jinja",
            form=topic_form,
            error=msg.get("topic_form_error")
        ),
        redbag_form=render_template(
            "admin/redbag.jinja",
            form=redbag_form,
            error=msg.get("redbag_form_error")
        ),
        topics=Topic.select(),
        redbags=Redbag.select()
    )


@admin.route("/")
@admin_required
def index():
    return render_dashboard()


@admin.get("/login")
def show_login_form():
    return render_template("admin/login.jinja", form=LoginForm())


@admin.post("/login")
def admin_login():
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
    form = TopicCreateForm()
    if not form.validate_on_submit():
        return render_dashboard(
            {"topic_form_error": "非法输入, 请检查"},
            topic_form=form,
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
            topic_form=form,
        )
    return render_dashboard()


@admin.post("/create_redbag")
@admin_required
def create_redbag():
    form = RedbagCreateForm()
    if not form.validate_on_submit():
        return render_dashboard(
            {"redbag_form_error": "非法输入, 请检查"},
            redbag_form=form,
        )
    try:
        Redbag.insert(
            name=form.name.data,
            password=form.password.data,
        ).execute()
    except IntegrityError:
        return render_dashboard(
            {"redbag_form_error": "重复的红包口令"},
            redbag_form=form,
        )
    return render_dashboard()


@admin.post("/del_topic")
@admin_required
def del_topic():
    form = TopicDeleteForm()
    if not form.validate_on_submit():
        return render_dashboard()
    topic: Topic = Topic.get_or_none(
        Topic.id == form.topic_id.data
    )
    if not topic:
        return "你要干嘛?"
    try:
        topic.delete_instance()
    except:
        return "删除失败"
    return render_dashboard()


@admin.post("/del_redbag")
@admin_required
def del_redbag():
    form = RedbagDeleteForm()
    if not form.validate_on_submit():
        return render_dashboard()
    redbag: Redbag = Redbag.get_or_none(
        Redbag.id == form.redbag_id.data
    )
    if not redbag:
        return "你要干嘛?"
    try:
        topics_need_redbag = (Topic
                              .select()
                              .where(Topic.redbag == redbag))
        for topic in topics_need_redbag:
            topic.delete_instance()
        redbag.delete_instance()
    except:
        return "删除失败, 你可能需要先把对应该红包的题目删除"
    return render_dashboard()
