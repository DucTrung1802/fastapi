from fastapi import Request
from fastapi.responses import JSONResponse

from ..utils.exceptions import GenericException


async def generic_exception_handler(request: Request, exception: GenericException):
    return JSONResponse(
        status_code=501,
        content={"message": f"Something went wrong with name: {exception.name}"},
    )
