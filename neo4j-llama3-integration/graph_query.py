from llama_index.core import StorageContext, Settings
from llama_index.llms.together import TogetherLLM

from llama_index.vector_stores.neo4jvector import Neo4jVectorStore


from dotenv import load_dotenv
import os

load_dotenv()

import openai




def query_graph(query, index):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response


"""
def query_graph_llama3(query):
    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    embed_dim = 1536

    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)


    #Settings.embed_model = HuggingFaceEmbedding(
    #    model_name="hkunlp/instructor-base", #"BAAI/bge-small-en-v1.5", 
    #    use_auth_token=os.getenv("HUGGINGFACE_API_KEY")
    #)

    llm = TogetherLLM(model="meta-llama/Meta-Llama-3-8B", api_key=os.getenv("LLAMA_API_KEY"))

    storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
    index = VectorStoreIndex.from_documents(
        storage_context=storage_context
    )

    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response
"""