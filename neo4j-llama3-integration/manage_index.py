from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core import StorageContext, load_index_from_storage

import os
from dotenv import load_dotenv

from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore


# create storage context using default stores


def store_index(index): 

    index.storage_context.persist()


def load_index():
    load_dotenv()
    graph_store = Neo4jPropertyGraphStore(
        username = os.getenv("NEO4J_USERNAME"),
        password = os.getenv("NEO4J_PASSWORD"),
        url = os.getenv("NEO4J_URI")
    )
    storage_context = StorageContext.from_defaults(graph_store=graph_store)
    return load_index_from_storage(storage_context)