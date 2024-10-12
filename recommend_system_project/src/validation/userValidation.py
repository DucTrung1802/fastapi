from pydantic import ValidationError

from ..models.neo4j import neo4j_models


async def validate_login(email: str, password: str):
    try:
        user = neo4j_models.User(email=email, password=password)
        _ = user.model_dump()
    except ValidationError as e:
        print("Validation errors:", e.json())
