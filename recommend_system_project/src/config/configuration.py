from datetime import timedelta

from ..utils import enums

# CONFIGURATION PARAMETERS

ENABLE_LOGGING = False
TOKEN_LOCATION = enums.TokenLocation.HEADER
ACCESS_TOKEN_LIFETIME = timedelta(hours=1)
REFRESH_TOKEN_LIFETIME = timedelta(days=14)
COOKIES_LIFETIME = timedelta(days=14)  # same as refresh token
X_API_KEY_HEADER = "x-api-key"
JWT_ALGORITHM = "HS256"
NEO4J_DB_URI = "neo4j://localhost:7687"
