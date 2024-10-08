from neontology import init_neontology


def initialize_neo4j(uri: str = None, user: str = None, password: str = None):
    try:
        init_neontology(uri, user, password)
    except Exception as e:
        print(f"Exception: {e}")
