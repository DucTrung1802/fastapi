from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..controller import userController

router = APIRouter()

TAG_NAME = "users"


@router.post("/login", tags=[TAG_NAME])
async def login(request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await userController.login(request)


@router.post("/verify_token", tags=[TAG_NAME])
async def verify_token(request: str):
    return await userController.verify_token(request)
