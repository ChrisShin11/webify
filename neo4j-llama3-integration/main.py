import graph_constructor
import graph_query
from graph_query import query_graph
from graph_constructor import construct_nodes_from_documents_init

from test_neo4j_db import test_neo4j_db

from dotenv import load_dotenv
import os

from llama_index.core import StorageContext, Settings



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
        print(index)
        print("Error in constructing nodes from documents.")
        return


    query = "What are the similarities between cats and llamas?"

    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)
    response = query_graph(query, index)
    print("GPT response: \n", response)

    Settings.llm = TogetherLLM(model="meta-llama/Llama-3-8b-chat-hf", api_key=os.getenv("LLAMA_API_KEY"))
    response = query_graph(query, index)
    print("LLama3 response: \n", response)








if __name__=="__main__":
    main()