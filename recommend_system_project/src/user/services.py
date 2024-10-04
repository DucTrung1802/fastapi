from .models import *
from ..utils.utils import *
from ..configurations import Configuration
from ..database.neo4j_db import Neo4jConnection
from ..neontology import Patient

# Initialize configuration
config = Configuration()
neo4j_config = config.get_neo4j_configuration()

# Create a Neo4j connection using environment variables
neo4j_connection = Neo4jConnection(
    uri=neo4j_config["uri"],
    user=neo4j_config["user"],
    password=neo4j_config["password"],
)


async def create_user_service(input_data: NewUser):
    patient = Patient.match(input_data.user_name)

    if not patient:
        result = Patient(
            username=input_data.user_name, password=input_data.password
        ).create()

    return {"message": "Patient created successfully", "data": result}
