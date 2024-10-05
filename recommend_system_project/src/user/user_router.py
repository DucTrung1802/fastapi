from fastapi import APIRouter
from .user_services import *
from .user_models import NewUser

router = APIRouter()


@router.post("/create_user/", tags=["users"])
async def create_user_route(input_data: NewUser):
    return await create_user_service(input_data)
