
class InternetConnectionError(Exception):
    def __init__(self, msg):
        self.msg = msg


class NumberOutOfRange(Exception):
    def __init__(self, msg):
        self.msg = msg


class NameNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg
