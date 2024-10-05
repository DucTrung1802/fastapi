from pydantic import BaseModel
from typing import Optional
from .utils.enums import *


class Token(BaseModel):
    token_type: str
    access_token: str


class Response(BaseModel):
    status: ResponseStatus
    message: str
    data: Optional[dict] = None
