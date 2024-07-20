from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core import StorageContext, load_index_from_storage

# create storage context using default stores


def store_index(): 
    storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore(),
        vector_store=SimpleVectorStore(),
        index_store=SimpleIndexStore(),
    )
    storage_context.persist()


def load_index():
    storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore.from_persist_dir(),
        #vector_store=SimpleVectorStore.from_persist_dir(),
        index_store=SimpleIndexStore.from_persist_dir(),
    )
    return load_index_from_storage(storage_context)