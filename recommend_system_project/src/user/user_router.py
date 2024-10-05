from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from .user_services import *
from .user_models import CreateUserModel


router = APIRouter()

TAG_NAME = "users"


@router.post("/create_user", tags=[TAG_NAME])
async def create_user(input_data: CreateUserModel):
    return await create_user_service(input_data)


@router.post("/login", tags=[TAG_NAME])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login_service(form_data)
