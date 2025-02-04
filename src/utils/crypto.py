import hashlib
import secrets
import os
from flask import current_app as app


def md5(content: str) -> str:
    content += app.config["md5"]["salt"]
    return hashlib.md5(content.encode()).hexdigest()


def gen_secret_key() -> str:
    """生成 secret_key"""
    words = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    key_length = 32
    if os.path.exists(".secret_key"):
        with open(".secret_key", "r") as file:
            key = file.read()
        if len(key) != key_length:
            raise ValueError("Key file contents corrupted")
    else:
        key = ''.join([secrets.choice(words) for _ in range(key_length)])
        with open(".secret_key", "w") as file:
            file.write(key)
        os.chmod(".secret_key", 0o600)
    return key

