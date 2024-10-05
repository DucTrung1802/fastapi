from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from .user_services import *
from .user_models import CreateUserModel
from ..dependencies import get_current_active_user


router = APIRouter()

TAG_NAME = "users"


@router.post("/create_user", tags=[TAG_NAME], response_model=Response)
async def create_user(input_data: CreateUserModel):
    return await create_user_service(input_data)


@router.post("/login", tags=[TAG_NAME], response_model=Response)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login_service(form_data)


@router.get("/get_secret_key", tags=[TAG_NAME])
async def get_secret_key(
    _: Annotated[Patient, Depends(get_current_active_user)],
):
    return await get_secret_key_service()
