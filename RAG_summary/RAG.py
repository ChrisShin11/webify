from llama_index.llms.together import TogetherLLM
import os

os.environ['TOGETHER_API_KEY'] = '9e9eecb88b9ea4f2d83d1a8bcd37caf6656c2d599cab02baf09ef6d96685914e'

import json

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_objects_as_text_files(json_data, output_dir):
    if json_data is None:
        return

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

# File path to the local JSON file
file_path = os.path.join('RAG_summary/data/workers.json')
output_dir = 'RAG_summary/data/'  # Directory where text files will be saved

# Read JSON data from the local file
json_data = read_json_from_file(file_path)

# Save JSON objects as text files
key_list = save_json_objects_as_text_files(json_data, output_dir)

from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
from llama_index.core.node_parser import SentenceSplitter

employee_docs = []
for name in key_list:
    path = os.path.join(f'RAG_summary/data/{name}.txt')
    docs = SimpleDirectoryReader(input_files =[path]).load_data()
    docs[0].doc_id = name
    employee_docs.extend(docs)

llm = TogetherLLM(
    model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo", api_key="9e9eecb88b9ea4f2d83d1a8bcd37caf6656c2d599cab02baf09ef6d96685914e"
)

splitter = SentenceSplitter(chunk_size=1024)

os.environ["OPENAI_API_KEY"] = 'sk-None-YooJu1Nf3u9MKjvbct01T3BlbkFJQtdfVox3UiITzuMoJaLp'

response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True
)
doc_summary_index = DocumentSummaryIndex.from_documents(
    employee_docs,
    llm=llm,
    transformations=[splitter],
    response_synthesizer=response_synthesizer,
    show_progress=True,
)

doc_summary_index.get_document_summary("Alice_Johnson")

doc_summary_index.storage_context.persist("index")