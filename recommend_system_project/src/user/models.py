from pydantic import BaseModel


class NewUser(BaseModel):
    user_name: str
    password: str
