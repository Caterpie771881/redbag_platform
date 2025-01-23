import hashlib
import random
import os
from flask import current_app as app


def md5(content: str) -> str:
    # content += app.config["md5"]["salt"]
    return hashlib.md5(content.encode()).hexdigest()


def gen_secret_key() -> str:
    words = "abcdefghijklmnopqrstuvwxyz0123456789"
    if os.path.exists(".secret_key"):
        with open(".secret_key", "r") as file:
            key = file.read()
    else:
        key = ''.join([random.choice(words) for _ in range(12)])
        with open(".secret_key", "w") as file:
            file.write(key)
    return key

