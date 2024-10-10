from typing import Annotated
from fastapi import APIRouter, Depends, Request
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


@router.put("/refresh_token", tags=[TAG_NAME])
async def refresh_token(request: Annotated[authMiddleware.is_authorized, Depends()]):
    return await userController.refresh_token(request)


@router.get("/get_data", tags=[TAG_NAME])
async def get_data(request: Annotated[authMiddleware.is_authorized, Depends()]):
    return await userController.get_data(request)
