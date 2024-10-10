from fastapi import Request, HTTPException, status
import jwt

from ..providers import jwtProvider
from ..config import configuration
from ..utils import enums

TOKEN_LOCATION = configuration.TOKEN_LOCATION


# This function will serve as a middleware or dependency to check authorization
async def is_authorized(request: Request):
    access_token = None

    # Method 1: Get access token from Authorization header
    if not TOKEN_LOCATION or TOKEN_LOCATION == enums.TokenLocation.HEADER:
        access_token = request.headers.get("Authorization")
        if access_token:
            access_token = access_token.replace("Bearer ", "")

    # Method 2: Get access token from cookies
    elif TOKEN_LOCATION == enums.TokenLocation.COOKIES:
        access_token = request.cookies.get("access_token")

    # Handle tokens
    try:
        payload = jwtProvider.verify_token(
            access_token, "KBgJwUETt4HeVD05WaXXI9V3JnwCVP"
        )
        request.state.data = payload

    # Access token is expired, return HTTP code 410 Gone for FE to call refreshToken API
    except jwt.ExpiredSignatureError:
        x_api_key = request.headers.get("x-api-key")
        if not x_api_key or x_api_key != "ductrung":
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Need to refresh token.",
            )
        else:
            return request

    # Other errors, return HTTP code 401 Unauthorized
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized.",
        )

    return request
