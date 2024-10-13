from password_validator import PasswordValidator
from email_validator import validate_email


PASSWORD_VALIDATOR = PasswordValidator()
PASSWORD_VALIDATOR.min(8)  # Minimum length 8
PASSWORD_VALIDATOR.no().spaces()  # No spaces allowed


async def validate_login(email: str, password: str):
    valid_email = validate_email(email)
    email = valid_email.email  # Extract the normalized email
    password = PASSWORD_VALIDATOR.validate(password)
