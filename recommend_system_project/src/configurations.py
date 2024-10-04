import os
from .utils.constants import *


NEO4J_URI = "neo4j://localhost:7687"


class Configuration:
    def __init__(self):
        self.neo4j_uri = NEO4J_URI

    def get_environment_variable(self, variable_name: str):
        return os.getenv(variable_name)

    def get_neo4j_configuration(self):
        neo4j_uri = self.neo4j_uri
        neo4j_user = self.get_environment_variable(NEO4J_USERNAME_ENV_KEY)
        neo4j_password = self.get_environment_variable(NEO4J_PASSWORD_ENV_KEY)

        return {"uri": neo4j_uri, "user": neo4j_user, "password": neo4j_password}
