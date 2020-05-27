import traceback

class ErrorCodeException(Exception):
    def __init__(self, error_code, message):
        self.error_code = -1
        self.message = message

        try:
           error_code = int(error_code) 
        except:
            pass

        if type(error_code) == int and error_code > 0:
            error_code = error_code * -1
        
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return repr(str(self.error_code) + " " + self.message)
