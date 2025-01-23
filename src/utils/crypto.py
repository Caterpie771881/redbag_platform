import hashlib
import random
from flask import current_app as app


def md5(content: str) -> str:
    # content += app.config["md5"]["salt"]
    return hashlib.md5(content.encode()).hexdigest()


def gen_secret_key() -> str:
    words = "abcdefghijklmnopqrstuvwxyz0123456789"
    key = ''.split([random.choice(words) for _ in range(12)])
    return key

