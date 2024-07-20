from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
import json
import os
from env import ROOT_DIR, SPLITTER_CHUNK_SIZE


def get_doc_index(llm, overwrite_index=False):
    
    try:
        storage_context = StorageContext.from_defaults(persist_dir="index")
        
    except FileNotFoundError as e:
        overwrite_index = True
    
    if overwrite_index:
        pass
    else:
        return load_index_from_storage(storage_context)
    
    docs = _json_to_docs(target='workers.json')
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

def _json_to_docs(target='workers.json'):
    file_path = os.path.join(ROOT_DIR, 'data', target)
    output_path = os.path.join(ROOT_DIR, 'data')
    
    json_data = _read_json_from_file(file_path)
    
    key_list = _save_json_objects_as_text_files(json_data, output_path)
    
    employee_docs = []
    for name in key_list:
        path = os.path.join(ROOT_DIR, 'data',f'{name}.txt')
        docs = SimpleDirectoryReader(input_files =[path]).load_data()
        docs[0].doc_id = name
        employee_docs.extend(docs)
        
    return employee_docs


def _save_json_objects_as_text_files(json_data, output_dir):
    if json_data is None:
        raise ValueError('No documents available.')

    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    key_list = []
    for key, value in json_data.items():
        name = value.get("name", f"entry_{key}").replace(" ", "_")  # Use name or fallback to entry_<key>
        file_path = os.path.join(output_dir, f"{name}.txt")
        
        key_list.append(name)
        # Convert JSON object to formatted string
        value_str = json.dumps(value, indent=4)
        
        # Write the string to a text file
        with open(file_path, 'w') as file:
            file.write(value_str)
        
        print(f"Saved {file_path}")
        
    return key_list

def _read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)