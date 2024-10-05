from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

from .user_models import *
from ..dependencies import timedelta, create_access_token
from ..models import *
from ..utils.utils import *
from ..configurations import ACCESS_TOKEN_EXPIRE_MINUTES
from ..database.neo4j_models import Patient
from ..utils.enums import *


async def create_user_service(input_data: CreateUserModel):
    # Validate input password
    if not validate_password(input_data.password):
        return Response(
            status=ResponseStatus.ERROR,
            message="Password length must be between 8 to 20 characters, has lowercase, uppercase characters and numbers.",
        ).model_dump(exclude={"data"})

    if not is_validate_email(input_data.email):
        return Response(
            status=ResponseStatus.ERROR,
            message="Email is invalid.",
        ).model_dump(exclude={"data"})

    # Check if the user_name already exists
    patient = Patient.match(input_data.user_name)

    # If patient does not exist, create new a patient
    if not patient:
        input_data.password = hash_password(input_data.password)
        result = Patient(
            username=input_data.user_name,
            password=input_data.password,
            email=input_data.email,
        ).create()

        return Response(
            status=ResponseStatus.SUCCESS,
            message="Patient created successfully.",
            data={
                "username": result.username,
            },
        )

    return Response(
        status=ResponseStatus.ERROR,
        message="Patient already exists.",
    ).model_dump(exclude={"data"})


async def login_service(input_data: OAuth2PasswordRequestForm):
    # Check if user_name already exists
    patient = Patient.match(input_data.username)

    if patient:
        # Verify password
        if verify_password(
            stored_password=patient.password, provided_password=input_data.password
        ):
            # Provide token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": input_data.username}, expires_delta=access_token_expires
            )
            token = Token(token_type="bearer", access_token=access_token)

            return Response(
                status=ResponseStatus.SUCCESS,
                data={"token": token},
            ).model_dump(exclude={"message"})

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_secret_key_service():
    return Response(
        status=ResponseStatus.SUCCESS,
        data={"secret_key": "hello world"},
    ).model_dump(exclude={"message"})
