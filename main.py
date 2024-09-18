from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

# Constants for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI app initialization
app = FastAPI()

# OAuth2PasswordBearer is a dependency class we use to extract the bearer token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Token generation function
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Pydantic model for Token
class Token(BaseModel):
    access_token: str
    token_type: str


# Endpoint to create a token
@app.post("/token", response_model=Token)
async def login():
    # In a real-world application, you'd verify user credentials here

    # Example user data to encode into the token
    user_data = {"sub": "user@example.com"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=user_data, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


# Dependency to verify the token
def verify_token(token: str = Depends(oauth2_scheme)):
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
    except jwt.PyJWTError:
        raise credentials_exception

    return username


# Protected route that requires a valid bearer token
@app.get("/users/me")
async def read_users_me(username: str = Depends(verify_token)):
    return {"username": username}


# Run the FastAPI app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
