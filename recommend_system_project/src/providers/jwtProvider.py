from datetime import datetime, timedelta, timezone

import jwt


def generate_token(data: dict, secret_key: str, token_life: timedelta):
    issue_at_time = int(datetime.now(timezone.utc).timestamp())
    expiration_time = int((datetime.now(timezone.utc) + token_life).timestamp())
    data_copy = data.copy()
    data_copy.update({"iat": issue_at_time, "exp": expiration_time})

    return jwt.encode(data_copy, secret_key)


def verify_token(token: str, secret_key: str):
    return jwt.decode(token, secret_key, algorithms="HS256")
