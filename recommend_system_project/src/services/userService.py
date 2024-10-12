from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from ..models.neo4j import neo4j_models
from ..config import environment, configuration
from ..providers import jwtProvider
from ..config import configuration
from ..utils import enums
from ..models.userModels import *

TOKEN_LOCATION = configuration.TOKEN_LOCATION


async def login(request: OAuth2EmailPasswordRequestForm):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized."
    )

    #

    # Query username (unique) in database
    user = neo4j_models.User.match(pp=request.email)
    print(user)
    print(type(user))

    # if (
    #     request.username != MOCK_DATABASE["user"]["email"]
    #     or request.password != MOCK_DATABASE["user"]["password"]
    # ):
    #     raise unauthorized_exception

    # # Create payload to include in JWT token
    # user_info = {
    #     "id": MOCK_DATABASE["user"]["id"],
    #     "email": MOCK_DATABASE["user"]["email"],
    # }

    # # Create access token and refresh token
    # access_token = jwtProvider.generate_token(
    #     user_info,
    #     environment.ACCESS_TOKEN_SECRET_KEY,
    #     configuration.ACCESS_TOKEN_LIFETIME,
    # )

    # refresh_token = jwtProvider.generate_token(
    #     user_info,
    #     environment.REFRESH_TOKEN_SECRET_KEY,
    #     configuration.REFRESH_TOKEN_LIFETIME,
    # )

    # # USE ONE OF THESE: Local storage OR HTTP only cookie

    # response = None

    # # Local storage: Return user info and tokens
    # if not TOKEN_LOCATION or TOKEN_LOCATION == enums.TokenLocation.HEADER:
    #     response = JSONResponse(
    #         content={
    #             **user_info,
    #             "access_token": access_token,
    #             "refresh_token": refresh_token,
    #         }
    #     )

    # # HTTP only cookie for browser
    # # max_age is lifetime of cookie, could be equal to refresh_token lifetime
    # elif TOKEN_LOCATION == enums.TokenLocation.COOKIES:
    #     response = JSONResponse(content={**user_info})
    #     response.set_cookie(
    #         key="access_token",
    #         value=access_token,
    #         httponly=True,
    #         secure=True,
    #         samesite=None,
    #         max_age=configuration.COOKIES_LIFETIME.total_seconds() * 1000,
    #     )

    #     response.set_cookie(
    #         key="refresh_token",
    #         value=refresh_token,
    #         httponly=True,
    #         secure=True,
    #         samesite=None,
    #         max_age=configuration.COOKIES_LIFETIME.total_seconds() * 1000,
    #     )

    # return response


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

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh Token API failed.",
        )


async def get_data(request):
    return JSONResponse(content={"hello": "world"})
