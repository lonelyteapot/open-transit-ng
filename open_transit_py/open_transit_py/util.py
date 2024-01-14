class PlaceholderError(Exception):
    def __init__(self, message: str, *extra):
        self.message = message
        self.extra = extra
        self.args = [message, *extra]
