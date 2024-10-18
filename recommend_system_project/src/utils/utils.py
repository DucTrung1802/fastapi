import bcrypt


def hash_password(raw_password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(stored_password: str, provided_password: str):
    return bcrypt.checkpw(
        provided_password.encode("utf-8"), stored_password.encode("utf-8")
    )
