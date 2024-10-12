from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr


class OAuth2EmailPasswordRequestForm(OAuth2PasswordRequestForm):
    @property
    def email(self) -> EmailStr:
        return self.username  # OAuth2PasswordRequestForm uses 'username' for email
