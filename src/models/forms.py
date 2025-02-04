from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    IntegerField,
)
from wtforms.validators import (
    Length,
    DataRequired,
    EqualTo,
)


class LoginForm(FlaskForm):
    """管理员登录表单"""
    username = StringField(
        "用户名",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "密码",
        validators=[
            DataRequired(),
            Length(min=8, max=25)
        ]
    )


class TopicCreateForm(FlaskForm):
    """题目添加表单"""
    name = StringField(
        "标题",
        validators=[DataRequired()]
    )
    type = StringField(
        "方向",
        validators=[DataRequired()]
    )
    flag = StringField(
        "flag",
        validators=[DataRequired()]
    )
    redbag = SelectField(
        "红包",
        validators=[DataRequired()]
    )

    def __init__(self,*args,**kwargs):
        from models.database import Redbag
        super(TopicCreateForm, self).__init__(*args,**kwargs)
        self.redbag.choices = [(r.id, r.name) for r in Redbag.select()]


class RedbagCreateForm(FlaskForm):
    """红包添加表单"""
    name = StringField("红包名称")
    password = StringField(
        "口令",
        validators=[DataRequired()]
    )


class FlagSubmitFrom(FlaskForm):
    """flag 提交表单"""
    flag = StringField(
        "flag",
        validators=[DataRequired()]
    )
    token = StringField(
        "token",
        validators=[DataRequired()]
    )


class TopicDeleteForm(FlaskForm):
    """题目删除表单"""
    topic_id = IntegerField(
        "id",
        validators=[DataRequired()]
    )


class RedbagDeleteForm(FlaskForm):
    """红包删除表单"""
    redbag_id = IntegerField(
        "id",
        validators=[DataRequired()]
    )


class RedbagUpdateForm(FlaskForm):
    """红包更新表单"""
    redbag_id = IntegerField(
        "id",
        validators=[DataRequired()]
    )
    name = StringField(
        "红包名称",
        validators=[DataRequired()]
    )
    password = StringField(
        "口令",
        validators=[DataRequired()]
    )


class GetTokenForm(FlaskForm):
    """获取 token 表单"""
    password = StringField(
        "入场口令",
        validators=[DataRequired()]
    )
    name = StringField(
        "姓名",
        validators=[
            DataRequired(),
            Length(min=1, max=20)
        ]
    )


class EditAdminForm(FlaskForm):
    """编辑管理员信息 表单"""
    admin_id = IntegerField(
        "id",
        validators=[DataRequired()]
    )
    username = StringField(
        "username",
        id="edit_admin_username",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "new password",
        id="edit_admin_password",
        validators=[
            DataRequired(),
            Length(min=8, max=25),
        ]
    )


class AddAdminForm(FlaskForm):
    """添加管理员信息 表单"""
    username = StringField(
        "username",
        validators=[DataRequired()]
    )
    password = StringField(
        "password",
        validators=[
            DataRequired(),
            Length(min=8, max=25)
        ]
    )
