from typing import Annotated
from fastapi import APIRouter, Depends

from ..controller import userController
from ..middlewares import authMiddleware
from ..models.userModels import *
from ..validation import userValidation


router = APIRouter()

TAG_NAME = "users"


@router.post("/create_user", tags=[TAG_NAME])
async def create_user(request: Annotated[User, Depends()]):
    await userValidation.validate_create_user(
        request.full_name, request.email, request.password
    )

    return await userController.create_user(request)


@router.post("/login", tags=[TAG_NAME])
async def login(request: Annotated[OAuth2EmailPasswordRequestForm, Depends()]):
    await userValidation.validate_login(request.email, request.password)

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
