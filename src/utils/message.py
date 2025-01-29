from flask import Flask

class JinjaMessage():
    def __init__(self, type, content):
        self.type = type
        self.content = content
    
    def __str__(self):
        return self.content


class JinjaMessageSet(dict):
    def add(self, key: str, msg: JinjaMessage):
        if not self.get(key):
            self[key] = []
        self[key].append(msg)
        return self

    def add_error_msg(self, key: str, msg: str):
        msg = JinjaMessage("error", msg)
        return self.add(key, msg)
    
    def add_info_msg(self, key, msg: JinjaMessage):
        msg = JinjaMessage("info", msg)
        return self.add(key, msg)

    def init_app(self, app: Flask):
        app.msgs = self
        app.jinja_env.globals["msgs"] = self

        @app.before_request
        def clear_set():
            self.clear()


message_set = JinjaMessageSet()

