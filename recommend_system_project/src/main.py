from fastapi import FastAPI

from .user import user

# from .dependencies import get_query_token, get_token_header

app = FastAPI()

app.include_router(user.router)


# Run one of these in command line
# uvicorn recommend_system_project.src.main:app
# uvicorn recommend_system_project.src.main:app --host 0.0.0.0 --port 8000 --workers 4
