from typing import Literal
import os
from dotenv import load_dotenv

from llama_index.core import SimpleDirectoryReader
from llama_index.core import PropertyGraphIndex
from llama_index.core import StorageContext
from llama_index.core import KnowledgeGraphIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding

from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.readers.graphdb_cypher import GraphDBCypherReader


NEO4J_URI='neo4j+s://3a1c9e7a.databases.neo4j.io'
NEO4J_DATABASE=None
NEO4J_USERNAME='neo4j'
NEO4J_PASSWORD='3kaSmTCTTgq4KE7p8Nd8YEv16Qzih7qgzh07JbcLDWU'


LLAMA_API_KEY='9e9eecb88b9ea4f2d83d1a8bcd37caf6656c2d599cab02baf09ef6d96685914e'
OPENAI_API_KEY='sk-None-YooJu1Nf3u9MKjvbct01T3BlbkFJQtdfVox3UiITzuMoJaLp'


def log_unique_files_in_directory(directory_path, log_file_path):
    previously_logged_files = []
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            for line in f:
                previously_logged_files.append(line.strip())
    file_names = os.listdir(directory_path)
    added_files = []
    with open(log_file_path, 'a') as f:
        for file_name in file_names:
            if file_name not in previously_logged_files:
                f.write(file_name + '\n')
                added_files.append(file_name)
    return added_files



def construct_nodes_from_documents_init():
    # best practice to use upper-case
    entities = Literal["PERSON", "TASK", "DEPARTMENT", "POSITION", "PROJECT"]
    relations = Literal["WORKS_WITH", "WORKS_AS", "WORKS_FOR", "SUPERVISES", "SUPERVISED BY", "ASSIGNED_TO", "ASSOCIATED_WITH"]

    # define which entities can have which relations
    validation_schema = {
        "PERSON": ["ASSIGNED_TO", "WORKS_WITH", "WORKS_AS", "SUPERVISES", "SUPERVISED BY"],
        "TASK": ["ASSIGNED_TO", "ASSOCIATED_WITH"],
        "DEPARTMENT": ["ASSOCIATED_WITH", "ASSIGNED_TO"],
        "POSITION": ["ASSOCIATED_WITH", "ASSIGNED_TO"],
        "PROJECT": ["ASSIGNED_TO", "ASSOCIATED_WITH"],
    }

    kg_extractor = SchemaLLMPathExtractor(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0.0),
        possible_entities=entities,
        possible_relations=relations,
        kg_validation_schema=validation_schema,
        strict=True, # if false, allows for values outside of the schema
    )
    load_dotenv()
    graph_store = Neo4jPropertyGraphStore(
        username = os.getenv("NEO4J_USERNAME"),
        password = os.getenv("NEO4J_PASSWORD"),
        url = os.getenv("NEO4J_URI")
    )
    data_path = './neo4j-llama3-integration/data/'
    data_files = log_unique_files_in_directory(data_path, './neo4j-llama3-integration/trained_document_files.txt')
    
    if len(data_files) > 0:
        for i in range(len(data_files)):
            data_files[i] = data_path + data_files[i]
        documents = SimpleDirectoryReader(input_files = data_files).load_data()
        index = PropertyGraphIndex.from_documents(
            documents,
            kg_extractors=[kg_extractor],
            embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
            property_graph_store=graph_store,
            show_progress=True,
        )
        return index
    return "No new files to add to the graph."

def index_from_neo4j_graph():
    query = """
    MATCH p=()-[r]->()
    WHERE NOT type(r) = 'MENTIONS'
    RETURN p LIMIT 100;
    """
    load_dotenv()
    url = NEO4J_URI
    username = NEO4J_USERNAME
    password = NEO4J_PASSWORD
    database = NEO4J_DATABASE

    graph_store = Neo4jPropertyGraphStore(username, password, url)

    reader = GraphDBCypherReader(url, username, password, database)
    documents = reader.load_data(query)

    storage_context = StorageContext.from_defaults(graph_store = graph_store)

    index = KnowledgeGraphIndex.from_documents(
        documents,
        max_triplets_per_chunk=2, 
        storage_context=storage_context,
        include_embeddings=True,
        show_progress=True
    )


    return index

"""
def construct_nodes_from_documents_llama3():
    # best practice to use upper-case
    entities = Literal["PERSON", "PLACE", "ORGANIZATION"]
    relations = Literal["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"]

    # define which entities can have which relations
    validation_schema = {
        "PERSON": ["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"],
        "PLACE": ["HAS", "PART_OF", "WORKED_AT"],
        "ORGANIZATION": ["HAS", "PART_OF", "WORKED_WITH"],
    }

    kg_extractor = SchemaLLMPathExtractor(
        llm=TogetherLLM(model="cognitivecomputations/dolphin-2.5-mixtral-8x7b", api_key=os.getenv("LLAMA_API_KEY")),
        #"meta-llama/Meta-Llama-3-70B" "mistralai/Mixtral-8x7B-Instruct-v0.1" "meta-llama/Llama-3-8b-chat-hf"
        possible_entities=entities,
        possible_relations=relations,
        kg_validation_schema=validation_schema,
        # if false, allows for values outside of the schema
        # useful for using the schema as a suggestion
        strict=True,
    )
    load_dotenv()
    graph_store = Neo4jPropertyGraphStore(
        username = os.getenv("NEO4J_USERNAME"),
        password = os.getenv("NEO4J_PASSWORD"),
        url = os.getenv("NEO4J_URI")
    )
    data_path = './neo4j-llama3-integration/data/'
    documents = SimpleDirectoryReader(data_path).load_data()
    index = PropertyGraphIndex.from_documents(
        documents,
        kg_extractors=[kg_extractor],
        embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
        #embed_model=TogetherEmbedding(model_name="togethercomputer/m2-bert-80M-8k-retrieval", api_key=os.getenv("LLAMA_API_KEY")),
        property_graph_store=graph_store,
    )
"""