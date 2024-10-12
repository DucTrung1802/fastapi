from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from ..services import userService
from ..config import environment, configuration
from ..providers import jwtProvider
from ..config import configuration
from ..utils import enums
from ..models.userModels import *

TOKEN_LOCATION = configuration.TOKEN_LOCATION


async def login(request: OAuth2EmailPasswordRequestForm):
    return await userService.login(request)


async def logout(request):
    return userService.logout(request)


async def refresh_token(request: Request):
    return userService.refresh_token(request)


async def get_data(request):
    return JSONResponse(content={"hello": "world"})
