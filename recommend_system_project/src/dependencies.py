from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2
import jwt
from jwt.exceptions import InvalidTokenError

from .configurations import Configuration, SECRET_KEY, ALGORITHM
from .models import *
from .database.neo4j_models import *

configuration = Configuration()
configuration.get_environment_variable(SECRET_KEY)


oauth2_scheme = OAuth2()


async def get_user(username: str):
    try:
        patient = Patient.match(username)
        return patient is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.username)

    if user is None:
        raise credentials_exception
    return user
