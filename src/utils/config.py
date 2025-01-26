import os
import json


def load_config(path: str="config.json"):
    """导入配置文件"""
    with open(path, "r", encoding='utf-8') as config_file:
        config = json.load(config_file)
    return config


def make_db_url(db_config: dict, type: str="sqlite"):
    """生成 url 形式的数据库连接"""
    try:
        config = db_config[type]
    except:
        raise TypeError("Unknown Database Type")
    
    if type == "sqlite":
        path = config["path"]
        if not os.path.exists(path):
            open(path, "w").close()
        return f"sqlite:///{path}"
    elif type == "mysql":
        host = config["host"]
        port = config["port"]
        db = config["db"]
        user = config["user"]
        passwd = config["passwd"]
        return f"mysql://{user}:{passwd}@{host}:{port}/{db}"
    raise TypeError("Unsupport Database Type")

