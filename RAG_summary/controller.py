from env import ROOT_DIR
from index import get_doc_index
from helper import read_json_from_file
from chat_engine import get_rag_doc_summary_chat, doc_upload
import os
import json
from llama_index.core import Settings
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM

import threading
import time

def init():
    
    try:
        llm = TogetherLLM(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo", api_key=os.environ['TOGETHER_API_KEY']
        )   
        
        Settings.llm = llm
        Settings.embed_model = TogetherEmbedding(model_name="togethercomputer/m2-bert-80M-8k-retrieval",
                        api_key=os.environ['TOGETHER_API_KEY'])
        
        return llm 
    except Exception as e:
        print('Error loading model: '+ str(e))
        
        
def choose_task_type(llm, prompt):
    path = os.path.join(ROOT_DIR, 'tasks.json')
    tasks = json.dumps(read_json_from_file(path), indent=4)

    response = llm.complete(f"""Given the following task descriptions, and the following prompt, please output only a 1 or a 2 corresponding to the closest matching task.
                            Prompt: {prompt}. Task Descriptions: {tasks}. Do not output anything other than a 1 or 2.""")

    if str(response) == str(1):
        return 1
        
    elif str(response) == str(2):
        return 2
    else:
        print('Orchestration Failure')
    
    return 2

##needs to have threads and allow for doc insertion too, which triggers reloading of chat_engines
#this controller runs in one thread, doc insertion runs in another, and insertion triggers events that cause
#re-loading of chat_engines
def controller():
    llm = init()
    
    graph_index = None
    rag_doc_index = get_doc_index(llm)
    
    indices = [graph_index, rag_doc_index]    ## handling index here allows us to re-compute indices with respect to thread coordination
    chat_engine_functions = [None, get_rag_doc_summary_chat]
    chat_engines = [None, chat_engine_functions[1](indices[1])]
    
    
    while True:
        prompt = input('Prompt: ')
        if prompt.upper() == 'N':
            break
        
        chat_id = choose_task_type(llm, prompt)
        
        #Use chat store to maintain the same history until reset signal() - will require maintaining indices at this level
        #when doc_upload_thread triggers recalculation of index and then chat_engine, it awaits an event to be triggered on this side in order to continue receiving doc uploads
        # response = chat_engines[chat_id - 1].chat(prompt)
        response = chat_engines[1].chat(prompt)
        
        print(response)
        
def doc_upload_thread():
    pass

def interrupt_thread():
    pass
if __name__ == '__main__':  
    controller()