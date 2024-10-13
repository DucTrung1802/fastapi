from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator

from ..utils.exceptions import *


PASSWORD_VALIDATOR = PasswordValidator()
PASSWORD_VALIDATOR.min(8)  # Minimum length 8
PASSWORD_VALIDATOR.no().spaces()  # No spaces allowed


async def validate_login(email: str, password: str):
    try:
        valid_email = validate_email(email)
        email = valid_email.email

        is_password_validate = PASSWORD_VALIDATOR.validate(password)
        if not is_password_validate:
            raise PasswordNotValidException

    except EmailNotValidError:
        raise EmailNotValidException
