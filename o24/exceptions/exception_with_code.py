import traceback

class ErrorCodeException(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return repr(str(self.error_code) + " " + self.message)
