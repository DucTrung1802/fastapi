import bcrypt
from password_validator import PasswordValidator
from email_validator import validate_email, EmailNotValidError

validator = PasswordValidator()

# Define your password policy
validator.min(8)  # Minimum length
validator.max(20)  # Maximum length
validator.has().lowercase()  # Must have lowercase
validator.has().uppercase()  # Must have uppercase
validator.has().digits()  # Must have digits


def hash_password(raw_password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(stored_password: str, provided_password: str):
    return bcrypt.checkpw(
        provided_password.encode("utf-8"), stored_password.encode("utf-8")
    )


def validate_password(password: str):
    return validator.validate(password)


def is_validate_email(email: str):
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError as e:
        return False
