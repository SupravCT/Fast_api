

class BookException(Exception):
    pass

class InvaildToken(BookException):
    pass

class RevokedToken(BaseException):
    pass

class NoPermission(BookException):
    pass