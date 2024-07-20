import graph_constructor
import graph_query
from graph_query import query_graph, query_graph_llama3
from test_neo4j_db import test_neo4j_db

from dotenv import load_dotenv
import os


load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


def main(): 
    if not test_neo4j_db(url, username, password): 
        print("Neo4j database is not connected.")
        return

    #os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
    #openai.api_key = os.environ["OPENAI_API_KEY"]

    print(query_graph("How long do llamas live?"))
    #print(query_graph_llama3("What is a llama, please tell me now"))

    print("done")







if __name__=="__main__":
    main()