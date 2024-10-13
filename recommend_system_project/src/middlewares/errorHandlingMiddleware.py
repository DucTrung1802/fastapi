from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import List, Tuple, Callable
from email_validator import EmailNotValidError


# Define the generic exception handler
async def generic_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Something went wrong."},
    )


async def email_not_valid_error_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": f"Email is not valid."},
    )


# Exception - Exception Handler mappings
ExceptionHandlerMapping: List[Tuple[type, Callable]] = [
    (Exception, generic_exception_handler),
    (EmailNotValidError, email_not_valid_error_handler),
]
