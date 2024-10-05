import hashlib
from password_validator import PasswordValidator

hash_lib = hashlib.sha256()
validator = PasswordValidator()

# Define your password policy
validator.min(8)  # Minimum length
validator.max(20)  # Maximum length
validator.has().lowercase()  # Must have lowercase
validator.has().uppercase()  # Must have uppercase
validator.has().digits()  # Must have digits


def hash_string(input_string: str):
    hash_lib = hashlib.sha256()
    hash_lib.update(input_string.encode("utf-8"))
    return hash_lib.hexdigest()


def validate_password(password: str):
    return validator.validate(password)


if __name__ == "__main__":
    print(hash_string("hello"))
