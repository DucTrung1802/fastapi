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


@router.get("/get_data", tags=[TAG_NAME])
async def get_data(request: Annotated[authMiddleware.is_authorized, Depends()]):
    return await userController.get_data(request)
