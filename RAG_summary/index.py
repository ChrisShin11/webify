from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from helper import read_json_from_file, save_json_objects_as_text_files
import os
from env import ROOT_DIR, SPLITTER_CHUNK_SIZE

from graph_constructor import construct_nodes_from_documents_init, index_from_neo4j_graph

def get_doc_index(llm, overwrite_index=False):
    
    try:
        storage_context = StorageContext.from_defaults(persist_dir="index")
        
    except FileNotFoundError as e:
        overwrite_index = True
    
    if overwrite_index:
        pass
    else:
        return load_index_from_storage(storage_context)
    
    docs = get_docs('workers.json')
    splitter = SentenceSplitter(chunk_size=SPLITTER_CHUNK_SIZE)
    
    ##can make response synthesizer async
    response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True
    )
    doc_summary_index = DocumentSummaryIndex.from_documents(
        docs,
        llm=llm,
        transformations=[splitter],
        response_synthesizer=response_synthesizer,
        show_progress=True,
    )
    
    doc_summary_index.storage_context.persist("index")
    
    return doc_summary_index

#switching to pdf?
def get_docs(target):
    return _json_to_docs(target=target)

def _json_to_docs(target='workers.json'):
    file_path = os.path.join(ROOT_DIR, 'data', target)
    output_path = os.path.join(ROOT_DIR, 'data')
    
    json_data = read_json_from_file(file_path)
    
    key_list = save_json_objects_as_text_files(json_data, output_path)
    
    employee_docs = []
    for name in key_list:
        path = os.path.join(ROOT_DIR, 'data',f'{name}.txt')
        docs = SimpleDirectoryReader(input_files =[path]).load_data()
        docs[0].doc_id = name
        employee_docs.extend(docs)
        
    return employee_docs

def get_graph_index(overwrite_index=False):
    
    try:
        storage_context = StorageContext.from_defaults(persist_dir='storage')
                
    except FileNotFoundError as e:
        overwrite_index = True
    
    if overwrite_index:
        pass
    else:
        return load_index_from_storage(storage_context)
    
    vector_index = index_from_neo4j_graph()
    vector_index.storage_context.persist('graph_index')
    
    return vector_index