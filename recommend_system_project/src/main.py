from fastapi import FastAPI

from .config import configuration, environment, neo4j_db
from .routes import userRoute, recommendRoute
from .middlewares.errorHandlingMiddleware import ExceptionHandlerMapping
from .utils.logging import *

neo4j_db.init_neontology(
    environment.NEO4J_DB_URI,
    environment.NEO4J_DB_USERNAME,
    environment.NEO4J_DB_PASSWORD,
)

if configuration.ENABLE_LOGGING:
    initialize_logging()

app = FastAPI()

# Routers
app.include_router(userRoute.router)

app.include_router(recommendRoute.router)


# Exception handlers
for excection, excection_handler in ExceptionHandlerMapping:
    app.add_exception_handler(excection, excection_handler)

# Run one of these in command line
# uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-config=log_conf.yaml
# uvicorn src.main:app --log-config=log_conf.yaml
