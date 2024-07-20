from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

def test_neo4j_db(url, username, password) -> bool:

    with GraphDatabase.driver(url, auth=(username, password)) as driver:
        driver.verify_connectivity()
        print("Neo4j database is connected.")
        return True
