from flask import Blueprint
from flask import render_template
from flask import current_app as app
from models.forms import FlagSubmitFrom, GetTokenForm
from models.database import Topic, User, Setting, Solve
from utils.message import Message, MessageSet


user = Blueprint("user", __name__)


def render_flag_submit_form(msgs=MessageSet()):
    """渲染 flag 提交页面"""
    return render_template(
        "flag.jinja",
        form=FlagSubmitFrom(),
        msgs=msgs
    )


def render_get_token_form(msgs=MessageSet()):
    """渲染 token 获取页面"""
    return render_template(
        "token.jinja",
        form=GetTokenForm(),
        msgs=msgs
    )


@user.get("/")
def index():
    return render_template("index.html")


@user.get("/flag")
def show_flag_submit_form():
    return render_flag_submit_form()


@user.post("/flag")
def check_flag():
    form = FlagSubmitFrom()
    msgs = MessageSet()

    if not form.validate_on_submit():
        msgs.add("flag_submit_from", Message("error", "非法输入, 请检查"))
        return render_flag_submit_form(msgs)
    
    token = (form.token.data).strip()
    user: User = User.get_or_none(User.token == token)
    if not user:
        msgs.add("flag_submit_from", Message("error", "不存在的 token"))
        return render_flag_submit_form(msgs)
    
    finish_topic: Topic = Topic.get_or_none(Topic.flag == form.flag.data)
    if not finish_topic:
        msgs.add("flag_submit_from", Message("error", "Flag 错误"))
        return render_flag_submit_form(msgs)
    
    has_solve: Solve = finish_topic.has_solve_by(user)
    # 若已解出, 返回解出时记录的红包口令, 防止白嫖更新后的口令
    show_password = lambda pwd: f"恭喜你答对了, 领取你的奖励吧\n<code>{ pwd }</code>"
    if has_solve:
        return render_flag_submit_form(
            msgs.add(
                "flag_submit_from",
                Message("info", show_password(has_solve.old_redbag))
            ),
        )
    Solve.add_record(finish_topic, user)
    return render_flag_submit_form(
        msgs.add(
            "flag_submit_from",
            Message("info", show_password(finish_topic.redbag.password))
        ),
    )


@user.get("/token")
def show_get_token_form():
    """获取 token 的表单"""
    return render_get_token_form()


@user.post("/token")
def get_token():
    """获取 token"""
    form = GetTokenForm()
    msgs = MessageSet()
    if not form.validate_on_submit():
        msgs.add("get_token_form", Message("error", "非法输入, 请检查"))
        return render_get_token_form(msgs)
    
    if Setting.get_("enter_password") != form.password.data:
        msgs.add("get_token_form", Message("error", "错误的口令, 看下群聊吧"))
        return render_get_token_form(msgs)
    
    token = User.gen_token(form.name.data)
    msgs.add(
        "get_token_form",
        Message(
            "info",
            f"您的 token 为\n<code>{ token }</code>\n请牢记"
        )
    )
    return render_get_token_form(msgs)
