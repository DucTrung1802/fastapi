from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import List, Tuple, Callable

from ..utils.exceptions import *


# DEFINE THE BASIC EXCEPTION HANDLERS
async def bad_request_handler(request: Request, exception: Exception):
    # Add more handlers here
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Bad request."},
    )


async def unauthorized_exception_handler(request: Request, exception: Exception):
    # Add more handlers here
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Unauthorized."},
    )


async def generic_exception_handler(request: Request, exception: Exception):
    # Add more handlers here
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"Something went wrong."},
    )


# DEFINE THE SPECIFIC EXCEPTION HANDLERS
async def empty_string_exception_handler(
    request: Request, exception: EmptyStringException
):
    # Add more handlers here
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"The field {exception.field_name} must not be empty."},
    )


async def email_not_valid_exception_handler(
    request: Request, exception: EmailNotValidException
):
    # Add more handlers here
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Email is not valid."},
    )


async def password_not_valid_exception_handler(
    request: Request, exception: PasswordNotValidException
):
    # Add more handlers here
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Password is not valid."},
    )


# Exception - Exception Handler mappings
ExceptionHandlerMapping: List[Tuple[type, Callable]] = [
    (Exception, generic_exception_handler),
    (BadRequestException, bad_request_handler),
    (UnauthorizedException, unauthorized_exception_handler),
    (EmailNotValidException, email_not_valid_exception_handler),
    (PasswordNotValidException, password_not_valid_exception_handler),
]
