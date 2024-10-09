from fastapi import FastAPI

from .routes import userRoute

app = FastAPI()


app.include_router(userRoute.router)


# Run one of these in command line
# uvicorn recommend_system_project.src.main:app
# uvicorn recommend_system_project.src.main:app --host 0.0.0.0 --port 8000 --workers 4
