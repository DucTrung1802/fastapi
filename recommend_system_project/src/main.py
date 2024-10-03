from fastapi import Depends, FastAPI
from configuration import Configuration
from database.neo4j_db import Neo4jConnection

# from .dependencies import get_query_token, get_token_header

configuration = Configuration()

neo4j_username = configuration.get_environment_variale("NEO4J_USERNAME")
neo4j_password = configuration.get_environment_variale("NEO4J_PASSWORD")
neo4j_uri = "neo4j://localhost:7687"
neo4j_target_database = "neo4j"

neo4j_conn = Neo4jConnection(neo4j_uri, neo4j_username, neo4j_password)

# app = FastAPI()


# Run one of these in command line
# uvicorn recommend_system_project.src.main:app
# uvicorn recommend_system_project.src.main:app --host 0.0.0.0 --port 8000 --workers 4
