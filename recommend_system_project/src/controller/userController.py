from fastapi import Request
from fastapi.responses import JSONResponse

from ..services import userService
from ..config import configuration
from ..models.userModels import *
from ..utils.exceptions import GenericException

TOKEN_LOCATION = configuration.TOKEN_LOCATION


async def login(request: OAuth2EmailPasswordRequestForm):
    try:
        return await userService.login(request)
    except:
        raise GenericException(name="hello")


async def logout(request):
    return userService.logout(request)


async def refresh_token(request: Request):
    return userService.refresh_token(request)


async def get_data(request):
    return JSONResponse(content={"hello": "world"})
