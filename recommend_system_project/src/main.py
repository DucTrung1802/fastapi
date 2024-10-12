from fastapi import FastAPI

from .config import configuration, environment, neo4j_db
from .routes import userRoute
from .utils.exceptions import *
from .middlewares.errorHandlingMiddleware import *

neo4j_db.init_neontology(
    configuration.NEO4J_DB_URI,
    environment.NEO4J_DB_USERNAME,
    environment.NEO4J_DB_PASSWORD,
)

app = FastAPI()

# Routers
app.include_router(userRoute.router)

# Exception handlers
app.add_exception_handler(GenericException, generic_exception_handler)

# Run one of these in command line
# uvicorn recommend_system_project.src.main:app
# uvicorn recommend_system_project.src.main:app --host 0.0.0.0 --port 8000 --workers 4
