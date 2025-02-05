from flask import Blueprint
from flask import render_template
from flask import current_app as app
from models.forms import FlagSubmitFrom, GetTokenForm
from models.database import Topic, User, Setting, Solve
from utils.auth import record_ip
from utils.message import message_set as msgs


user = Blueprint("user", __name__)


def render_flag_submit_form():
    """渲染 flag 提交页面"""
    return render_template(
        "flag.jinja",
        form=FlagSubmitFrom(),
    )


def render_get_token_form():
    """渲染 token 获取页面"""
    return render_template(
        "token.jinja",
        form=GetTokenForm(),
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

    if not form.validate_on_submit():
        msgs.add_error_msg("flag_submit_from", "非法输入, 请检查")
        return render_flag_submit_form()
    
    token = (form.token.data).strip()
    user: User = User.get_or_none(User.token == token)
    if not user:
        msgs.add_error_msg("flag_submit_from", "不存在的 token")
        return render_flag_submit_form()
    
    if user.ban:
        msgs.add_info_msg("flag_submit_from", "token 已被封禁, 请联系管理员")
        return render_flag_submit_form()
    
    finish_topic: Topic = Topic.get_or_none(Topic.flag == form.flag.data)
    if not finish_topic:
        msgs.add_error_msg("flag_submit_from", "Flag 错误")
        return render_flag_submit_form()
    
    has_solve: Solve = finish_topic.has_solve_by(user)
    # 若已解出, 返回解出时记录的红包口令, 防止白嫖更新后的口令
    show_password = lambda pwd: f"恭喜你答对了, 领取你的奖励吧\n<code>{ pwd }</code>"
    if has_solve:
        msgs.add_info_msg(
            "flag_submit_from",
            show_password(has_solve.old_redbag)
        )
        return render_flag_submit_form()
    Solve.add_record(finish_topic, user)
    msgs.add_info_msg(
        "flag_submit_from",
        show_password(finish_topic.redbag.password)
    )
    return render_flag_submit_form()


@user.get("/token")
def show_get_token_form():
    """获取 token 的表单"""
    return render_get_token_form()


@user.post("/token")
# @record_ip
def get_token():
    """获取 token"""
    form = GetTokenForm()

    if not form.validate_on_submit():
        msgs.add_error_msg("get_token_form", "非法输入, 请检查")
        return render_get_token_form()
    
    if Setting.get_("enter_password") != form.password.data:
        msgs.add_error_msg("get_token_form", "错误的口令, 看下群聊吧")
        return render_get_token_form()
    
    name = form.name.data
    token = User.gen_token(name)
    msgs.add_info_msg(
        "get_token_form",
        f"您的 token 为\n<code>{ token }</code>\n请牢记"
    )
    return render_get_token_form()
