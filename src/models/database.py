import peewee as pw
from playhouse.db_url import connect
from utils.config import load_config, make_db_url
from utils.crypto import md5


config = load_config()
db: pw.Database = connect(make_db_url(config["database"]))


class BaseModel(pw.Model):
    class Meta:
        database = db


class Admin(BaseModel):
    """管理员表"""
    username = pw.CharField(max_length=50, unique=True)
    password = pw.CharField(max_length=50)

    @classmethod
    def check(cls, username: str, password: str) -> "Admin":
        return Admin.get_or_none(
            Admin.username == username,
            Admin.password == md5(password)
        )


class TopicType(BaseModel):
    """题目类型"""
    content = pw.CharField(max_length=50, unique=True)


class Redbag(BaseModel):
    """红包表"""
    name = pw.CharField(max_length=50)
    password = pw.CharField(max_length=255, unique=True)


class Topic(BaseModel):
    """题目表"""
    name = pw.CharField(max_length=255, null=True)
    type = pw.ForeignKeyField(TopicType)
    redbag = pw.ForeignKeyField(Redbag)
    # XXX: 目前仅能建立 flag <-> redbag 的映射, flag 暂时只能唯一
    flag = pw.CharField(max_length=255, unique=True)

    @classmethod
    def create_topic(
            cls,
            name: str,
            type: str,
            redbag: str,
            flag: str
        ) -> "Topic":
        topic_type, created = TopicType.get_or_create(content=type)
        redbag = Redbag.get_or_none(Redbag.id == redbag)

        topic = Topic(
            name=name,
            flag=flag,
            type=topic_type,
            redbag=redbag,
        )
        return topic
    
    def has_solve_by(self, user: "User") -> bool:
        if Solve.get_or_none(
            Solve.user == user,
            Solve.topic == self
        ):
            return True
        return False


class User(BaseModel):
    """普通用户表"""
    username = pw.CharField(max_length=50)
    token = pw.CharField(max_length=50, unique=True)

    @classmethod
    def gen_token(cls, name) -> str:
        from time import time
        from random import random
        token = md5(str(time()))
        while User.get_or_none(User.token == token):
            token = md5(str(time()) + str(random()))
        User.create(username=name, token=token)
        return token


class Solve(BaseModel):
    """记录已解出题目的表格"""
    topic = pw.ForeignKeyField(Topic, backref='who_solve_me')
    user = pw.ForeignKeyField(User, backref='topic_has_solve')


class Setting(BaseModel):
    """存放全局设置"""
    key = pw.TextField(unique=True)
    value = pw.TextField(null=True)

    @classmethod
    def get_(cls, key: str, default=None):
        setting = Setting.get_or_none(Setting.key == key)
        if setting:
            return setting.value
        return default
    
    @classmethod
    def set_(cls, key: str, value: str):
        Setting(key=key, value=value).save()


def db_init():
    """初始化数据库"""
    with db:
        db.create_tables([
            Admin,
            TopicType,
            Redbag,
            Topic,
            Setting,
            User,
            Solve,
        ])
        if not Setting.get_("first_launch"):
            default_user = config["default_user"]
            user = Admin(
                username=default_user["username"],
                password=md5(default_user["password"])
            )
            user.save()
            Setting.set_("first_launch", True)

            enter_password = config["enter_password"]
            Setting.set_("enter_password", enter_password)

