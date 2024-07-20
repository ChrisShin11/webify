import graph_constructor
import graph_query
from graph_query import query_graph
from graph_constructor import construct_nodes_from_documents_init

from test_neo4j_db import test_neo4j_db

from dotenv import load_dotenv
import os


from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage


load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


def main(): 
    if not test_neo4j_db(url, username, password): 
        print("Neo4j database is not connected.")
        return


    index = construct_nodes_from_documents_init()


    print("done")







if __name__=="__main__":
    main()