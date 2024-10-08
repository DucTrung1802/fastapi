from pydantic import BaseModel


class CreateUserModel(BaseModel):
    user_name: str
    password: str
    email: str
