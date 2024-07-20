from typing import Literal
import os
from dotenv import load_dotenv

from llama_index.core import SimpleDirectoryReader
from llama_index.core import PropertyGraphIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding

from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore



def log_unique_files_in_directory(directory_path, log_file_path):
    previously_logged_files = []
    with open(log_file_path, 'r') as f:
        for line in f:
            previously_logged_files.append(line.strip())
    file_names = os.listdir(directory_path)
    added_files = []
    with open(log_file_path, 'w') as f:
        for file_name in file_names:
            if file_name not in previously_logged_files:
                f.write(file_name + '\n')
                added_files.append(file_name)
    return added_files



def construct_nodes_from_documents_init():
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
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0.0),
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
        show_progress=True,
    )

    log_unique_files_in_directory(data_path, './neo4j-llama3-integration/trained_document_files.txt')

    return index



def construct_nodes_from_additional_documents(data_path, index):
    new_training_data = log_unique_files_in_directory(data_path, './neo4j-llama3-integration/trained_document_files.txt')




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