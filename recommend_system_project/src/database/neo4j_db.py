from neo4j import GraphDatabase, Record
import typing as t


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

        # Validate the connection
        session = self.driver.session()
        response = session.run("RETURN 1")
        result = [record for record in response]
        if len(result) < 1:
            raise Exception("Neo4j connection is not established")

    def query(self, database: str, query: str, parameters: dict[str, t.Any] = None):
        session = None
        response = None
        try:
            session = self.driver.session(database=database)
            response = session.run(query=query, parameters=parameters)
            result = [record for record in response]
            print(f"Query successful: returning {len(result)} records")
            return result  # Collect the records
        except Exception as e:
            print(f"Query failed: {e}")
        finally:
            if session:
                session.close()
        return response

    def close(self):
        self.driver.close()
