from fastapi import HTTPException
from .user_models import *
from ..models import *
from ..utils.utils import *
from ..configurations import Configuration
from ..database.neo4j_repository import initialize_neo4j
from ..database.neo4j_models import Patient
from ..utils.enums import *

# Initialize configuration
config = Configuration()
neo4j_config = config.get_neo4j_configuration()

# Create a Neo4j connection using environment variables
neo4j_connection = initialize_neo4j(
    uri=neo4j_config["uri"],
    user=neo4j_config["user"],
    password=neo4j_config["password"],
)


async def create_user_service(input_data: NewUser) -> Response:
    # Validate input password
    if not validate_password(input_data.password):
        return Response(
            status=ResponseStatus.ERROR,
            message="Password length must be between 8 to 20 characters, has lowercase, uppercase characters and numbers",
        ).model_dump(exclude={"data"})

    # Check if the user_name already exists
    patient = Patient.match(input_data.user_name)

    # If patient does not exist, create new a patient
    if not patient:
        input_data.password = hash_string(input_data.password)
        result = Patient(
            username=input_data.user_name, password=input_data.password
        ).create()

        return Response(
            status=ResponseStatus.SUCCESS,
            message="Patient created successfully",
            data={
                "username": result.username,
            },
        )

    return Response(
        status=ResponseStatus.ERROR,
        message="Patient already exists",
    ).model_dump(exclude={"data"})
