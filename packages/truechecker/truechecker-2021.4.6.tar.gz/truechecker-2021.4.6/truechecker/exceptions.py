class TrueCheckerException(Exception):
    pass


class BadRequest(TrueCheckerException):
    pass


class Unauthorized(TrueCheckerException):
    pass


class AlreadyRunning(TrueCheckerException):
    pass


class ValidationError(TrueCheckerException):
    pass
