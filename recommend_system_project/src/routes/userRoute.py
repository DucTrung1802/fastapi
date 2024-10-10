from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..controller import userController
from ..middlewares import authMiddleware

router = APIRouter()

TAG_NAME = "users"


@router.post("/login", tags=[TAG_NAME])
async def login(request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await userController.login(request)


@router.delete("/logout", tags=[TAG_NAME])
async def logout(request: Annotated[authMiddleware.is_authorized, Depends()]):
    return await userController.logout(request)
