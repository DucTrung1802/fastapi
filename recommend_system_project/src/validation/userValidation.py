from pydantic import ValidationError

from ..models.neo4j import neo4j_models
from ..utils.exceptions import GenericException


async def validate_login(email: str, password: str):
    try:
        user = neo4j_models.User(email=email, password=password)
        _ = user.model_dump()
    except:
        raise GenericException(name="validation")
