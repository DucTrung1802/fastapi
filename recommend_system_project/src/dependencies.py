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


async def verify_token(token: str):
    try:
        # Decode the token to get the payload (i.e., user info)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Optionally, you can include checks for token expiration, etc.
        if "exp" in payload and payload["exp"] < datetime.now(timezone.utc).timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username = payload.get("sub")
        user = await get_user(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)  # Your token verification logic here
    if not user:
        # Raise 401 Unauthorized if the user is not authenticated
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
