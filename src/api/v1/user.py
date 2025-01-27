from flask import Blueprint
from flask import render_template
from flask import current_app as app
from models.forms import FlagSubmitFrom, GetTokenForm
from models.database import Topic, User, Setting, Solve


user = Blueprint("user", __name__)


@user.get("/")
def index():
    return render_template("index.html")


@user.get("/flag")
def show_flag_submit_form():
    return render_template("flag.jinja", form=FlagSubmitFrom())


@user.post("/flag")
def check_flag():
    form = FlagSubmitFrom()
    if not form.validate_on_submit():
        return render_template(
            "flag.jinja",
            form=form,
            error="非法输入, 请检查"
        )
    token = (form.token.data).strip()
    user: User = User.get_or_none(User.token == token)
    if not user:
        return render_template(
            "flag.jinja",
            form=form,
            error="不存在的 token"
        )
    finish_topic: Topic = Topic.get_or_none(Topic.flag == form.flag.data)
    if not finish_topic:
        return render_template(
            "flag.jinja",
            form=form,
            error="Flag 错误"
        )
    has_solve: Solve = finish_topic.has_solve_by(user)
    # 若已解出, 返回解出时记录的红包口令, 防止白嫖更新后的口令
    if has_solve:
        return render_template(
            "flag.jinja",
            form=form,
            password=has_solve.old_redbag
        )
    Solve.add_record(finish_topic, user)
    return render_template(
        "flag.jinja",
        form=form,
        password=finish_topic.redbag.password
    )


@user.get("/token")
def show_get_token_form():
    """获取 token 的表单"""
    return render_template("token.jinja", form=GetTokenForm())


@user.post("/token")
def get_token():
    """获取 token"""
    form = GetTokenForm()
    if not form.validate_on_submit():
        return render_template(
            "token.jinja",
            form=form,
            error="非法输入, 请检查"
        )
    if Setting.get_("enter_password") != form.password.data:
        return render_template(
            "token.jinja",
            form=form,
            error="错误的口令, 看下群聊吧"
        )
    token = User.gen_token(form.name.data)
    return render_template(
        "token.jinja",
        form=form,
        token=token
    )
