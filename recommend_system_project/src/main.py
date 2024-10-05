from fastapi import FastAPI

from .configurations import Configuration
from .database.neo4j_repository import initialize_neo4j
from .user import user_router

# from .dependencies import get_query_token, get_token_header

app = FastAPI()

# Initialize configuration
config = Configuration()
neo4j_config = config.get_neo4j_configuration()

# Create a Neo4j connection using environment variables
initialize_neo4j(
    uri=neo4j_config["uri"],
    user=neo4j_config["user"],
    password=neo4j_config["password"],
)

app.include_router(user_router.router)


# Run one of these in command line
# uvicorn recommend_system_project.src.main:app
# uvicorn recommend_system_project.src.main:app --host 0.0.0.0 --port 8000 --workers 4
