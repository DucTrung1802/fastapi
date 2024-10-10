from datetime import timedelta
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..providers import jwtProvider
from ..config import configuration
from ..utils import enums

TOKEN_LOCATION = configuration.TOKEN_LOCATION

MOCK_DATABASE = {
    "user": {
        "id": "ductrung-sample-id-1234",
        "email": "trung.lyduc18@gmail.com",
        "password": "abcd1234",
    }
}

ACCESS_TOKEN_SECRET_KEY = "KBgJwUETt4HeVD05WaXXI9V3JnwCVP"
REFRESH_TOKEN_SECRET_KEY = "fcCjhnpeopVn2Hg1jG75MUi62051yL"


async def login(request):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized."
    )

    if (
        request.username != MOCK_DATABASE["user"]["email"]
        or request.password != MOCK_DATABASE["user"]["password"]
    ):
        raise unauthorized_exception

    # Create payload to include in JWT token
    user_info = {
        "id": MOCK_DATABASE["user"]["id"],
        "email": MOCK_DATABASE["user"]["email"],
    }

    # Create access token and refresh token
    access_token_lifetime = timedelta(seconds=5)
    access_token = jwtProvider.generate_token(
        user_info, ACCESS_TOKEN_SECRET_KEY, access_token_lifetime
    )

    refresh_token_lifetime = timedelta(days=7)
    refresh_token = jwtProvider.generate_token(
        user_info, REFRESH_TOKEN_SECRET_KEY, refresh_token_lifetime
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
            max_age=refresh_token_lifetime.total_seconds() * 1000,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite=None,
            max_age=refresh_token_lifetime.total_seconds() * 1000,
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
            refresh_token, "fcCjhnpeopVn2Hg1jG75MUi62051yL"
        )

        # Create new access token
        access_token_lifetime = timedelta(hours=1)
        access_token = jwtProvider.generate_token(
            payload, ACCESS_TOKEN_SECRET_KEY, access_token_lifetime
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
                max_age=timedelta(days=7).total_seconds() * 1000,
            )

        return response

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh Token API failed.",
        )


async def get_data(request):
    return JSONResponse(content={"hello": "world"})
