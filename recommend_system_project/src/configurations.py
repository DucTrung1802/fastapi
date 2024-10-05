import os
from .utils.constants import *

# EXPLICIT CONFIGURATIONS
VERSION = "0.1.0"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"


NEO4J_URI = "neo4j://localhost:7687"


# CREDENTIALS KEYS
NEO4J_USERNAME_ENV_KEY = "NEO4J_USERNAME"
NEO4J_PASSWORD_ENV_KEY = "NEO4J_PASSWORD"
SECRET_KEY = "SECRET_KEY"


class Configuration:
    def __init__(self):
        pass

    def get_environment_variable(self, variable_name: str):
        return os.getenv(variable_name)

    def get_neo4j_configuration(self):
        neo4j_uri = NEO4J_URI
        neo4j_user = self.get_environment_variable(NEO4J_USERNAME_ENV_KEY)
        neo4j_password = self.get_environment_variable(NEO4J_PASSWORD_ENV_KEY)

        return {"uri": neo4j_uri, "user": neo4j_user, "password": neo4j_password}
