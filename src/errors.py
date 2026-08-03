from typing import Any,Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BookException(Exception):
    pass

class InvaildToken(BookException):
    pass

class RevokedToken(BookException):
    pass

class NoPermission(BookException):
    pass


def create_exception_handler(status_code:int,messages:Any):
    
    async def exception_handler(request:Request,exc:BookException):
        return JSONResponse(
            status_code=status_code,
            content={"message": messages}
        )
    return exception_handler
