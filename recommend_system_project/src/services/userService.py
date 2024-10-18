from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse

from ..config import configuration, environment
from ..models.neo4j import neo4j_models
from ..models.userModels import *
from ..providers import jwtProvider
from ..utils import enums, utils
from ..utils.exceptions import *

TOKEN_LOCATION = configuration.TOKEN_LOCATION


async def create_user(request: User):
    # Query email in database
    user = neo4j_models.User.match(pp=request.email)

    # If user already exists, return message
    if user:
        return JSONResponse(content={"message": "User already exists."})

    # Create new user
    request.password = utils.hash_password(request.password)
    new_user = neo4j_models.User(
        full_name=request.full_name, email=request.email, password=request.password
    ).merge()

    return JSONResponse(
        content={"message": f"A new user was created with email '{request.email}'"}
    )


async def login(request: OAuth2EmailPasswordRequestForm):
    # Query email in database
    user = neo4j_models.User.match(pp=request.email)

    if not user:
        raise UnauthorizedException

    # Verify password
    if not utils.verify_password(
        stored_password=user.password, provided_password=request.password
    ):
        raise UnauthorizedException

    # Create payload to include in JWT token
    user_info = {
        "email": user.email,
    }

    # Create access token and refresh token
    access_token = jwtProvider.generate_token(
        user_info,
        environment.ACCESS_TOKEN_SECRET_KEY,
        configuration.ACCESS_TOKEN_LIFETIME,
    )

    refresh_token = jwtProvider.generate_token(
        user_info,
        environment.REFRESH_TOKEN_SECRET_KEY,
        configuration.REFRESH_TOKEN_LIFETIME,
    )

    # USE ONE OF THESE: Local storage OR HTTP only cookie

    response = None

    # Local storage: Return user info and tokens
    if not TOKEN_LOCATION or TOKEN_LOCATION == enums.TokenLocation.HEADER:
        response = JSONResponse(
            content={
                **user_info,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )

    # HTTP only cookie for browser
    # max_age is lifetime of cookie, could be equal to refresh_token lifetime
    elif TOKEN_LOCATION == enums.TokenLocation.COOKIES:
        response = JSONResponse(content={**user_info})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite=None,
            max_age=configuration.COOKIES_LIFETIME.total_seconds() * 1000,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite=None,
            max_age=configuration.COOKIES_LIFETIME.total_seconds() * 1000,
        )

    return response


async def logout(request):
    # Clear cookies
    response = JSONResponse(
        content={"message": "Logout API success!"}, status_code=status.HTTP_200_OK
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


async def refresh_token(request: Request):
    # Local storage
    if not TOKEN_LOCATION or TOKEN_LOCATION == enums.TokenLocation.HEADER:
        body = await request.json()
        refresh_token = body.get("refresh_token")
        if refresh_token:
            refresh_token = refresh_token.replace("Bearer ", "")

    # HTTP only cookie for browser
    # max_age is lifetime of cookie, could be equal to refresh_token lifetime
    elif TOKEN_LOCATION == enums.TokenLocation.COOKIES:
        refresh_token = request.cookies.get("refresh_token")

    # Verify refresh token and get payload
    try:
        payload = jwtProvider.verify_token(
            refresh_token, environment.REFRESH_TOKEN_SECRET_KEY
        )

        # Create new access token
        access_token = jwtProvider.generate_token(
            payload,
            environment.ACCESS_TOKEN_SECRET_KEY,
            configuration.ACCESS_TOKEN_LIFETIME,
        )

        # Response: Local storage / HTTP only cookie for browser
        # USE ONE OF THESE: Local storage OR HTTP only cookie

        response = None

        # Local storage: Return user info and tokens
        if not TOKEN_LOCATION or TOKEN_LOCATION == enums.TokenLocation.HEADER:
            response = JSONResponse(
                content={
                    "access_token": access_token,
                }
            )

        # HTTP only cookie for browser
        # max_age is lifetime of cookie, could be equal to refresh_token lifetime
        elif TOKEN_LOCATION == enums.TokenLocation.COOKIES:
            response = JSONResponse(content={})
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite=None,
                max_age=configuration.COOKIES_LIFETIME.total_seconds() * 1000,
            )

        return response

    except:
        raise BadRequestException


async def get_data(request):
    return JSONResponse(content={"hello": "world"})
