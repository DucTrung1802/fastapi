from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from fastapi import Form


class OAuth2EmailPasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        email: str = Form(..., description="The email of the user"),
        password: str = Form(..., description="The password"),
    ):
        super().__init__(username="", password=password)
        self.email = email
