from pydantic import BaseModel
from typing import Optional, Union
from .utils.enums import *


class Token(BaseModel):
    token_type: str
    access_token: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Response(BaseModel):
    status: ResponseStatus
    message: Optional[str] = None
    data: Optional[dict] = None
