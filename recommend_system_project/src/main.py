from fastapi import FastAPI

from .config import configuration, environment, neo4j_db
from .routes import userRoute, recommendRoute
from .middlewares.errorHandlingMiddleware import ExceptionHandlerMapping

neo4j_db.init_neontology(
    configuration.NEO4J_DB_URI,
    environment.NEO4J_DB_USERNAME,
    environment.NEO4J_DB_PASSWORD,
)

app = FastAPI()

# Routers
app.include_router(userRoute.router)

app.include_router(recommendRoute.router)


# Exception handlers
for excection, excection_handler in ExceptionHandlerMapping:
    app.add_exception_handler(excection, excection_handler)

# Run one of these in command line
# uvicorn recommend_system_project.src.main:app
# uvicorn recommend_system_project.src.main:app --host 0.0.0.0 --port 8000 --workers 4
