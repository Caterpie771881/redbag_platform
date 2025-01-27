class Message():
    def __init__(self, type, content):
        self.type = type
        self.content = content


class MessageSet(dict):
    def add(self, key: str, msg: Message):
        if not self.get(key):
            self[key] = []
        self[key].append(msg)
        return self

