from neontology import init_neontology

from ..utils.logging import log


def initialize_neo4j(uri: str = None, user: str = None, password: str = None):
    try:
        init_neontology(uri, user, password)
    except Exception as e:
        log(f"Exception: {e}")
