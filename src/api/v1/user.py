from flask import Blueprint
from flask import render_template
from flask import current_app as app
from models.forms import FlagSubmitFrom
from models.database import Topic


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
    finish_topic = Topic.get_or_none(Topic.flag == form.flag.data)
    if finish_topic:
        return render_template(
            "flag.jinja",
            form=form,
            password=finish_topic.redbag.password
        )
    return render_template(
        "flag.jinja",
        form=form,
        error="Flag 错误"
    )
