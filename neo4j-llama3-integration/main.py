from dotenv import load_dotenv
import os

from test_neo4j_db import test_neo4j_db
from graph_query import query_graph
from graph_constructor import construct_nodes_from_documents_init
from manage_index import store_index, load_index

from llama_index.core import Settings
from llama_index.llms.together import TogetherLLM
from llama_index.llms.openai import OpenAI



load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


def main(): 
    if not test_neo4j_db(url, username, password): 
        print("Neo4j database is not connected.")
        return


    index = construct_nodes_from_documents_init()

    if type(index) == str:
        print("Error in constructing nodes from documents.")
        print(index)
        index = load_index()
    else: 
        store_index(index)

    query = "Give me a list of people in the engineering department?"

    print("Query: ", query)
    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)
    response = query_graph(query, index)
    print("GPT response: \n", response)

    Settings.llm = TogetherLLM(model="meta-llama/Llama-3-8b-chat-hf", api_key=os.getenv("LLAMA_API_KEY"))
    response = query_graph(query, index)
    print("LLama3 response: \n", response)





if __name__=="__main__":
    main()