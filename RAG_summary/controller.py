from env import ROOT_DIR
from index import get_doc_index
from helper import read_json_from_file
from chat_engine import get_rag_doc_summary_chat, doc_upload
import os
import json
from llama_index.core import Settings
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core import StorageContext

import threading
import time

indices = [None, None]
chat_engine_functions = [None, get_rag_doc_summary_chat]
chat_engines = [None, chat_engine_functions[1](indices[1])]

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

    print('Response: ' + str(response))

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
def controller(interrupt_event):
    global indices, chat_engine_functions, chat_engines
    
    llm = init()
    
    graph_index = None
    rag_doc_index = get_doc_index(llm)
    
    indices = [graph_index, rag_doc_index]    ## handling index here allows us to re-compute indices with respect to thread coordination
    
    api_event = threading.Event()
    return_event = threading.Event()
    
    #create threads - in reality I believe we will have three threads managed by the API, so this definition will have to be removed from here
    api_thread = threading.Thread(target=doc_upload_thread, args=(api_event, return_event), daemon=True)
    
    api_thread.start()
    
    while True:
        if interrupt_event.is_set():
            break
            
            
        prompt = input('Prompt: ')
        if prompt.upper() == 'N':
            break
    
        #will be thread behavior
        if api_event.is_set():
            new_doc(return_event)
        
        chat_id = choose_task_type(llm, prompt)
        
        #Use chat store to maintain the same history until reset signal() - will require maintaining indices at this level
        #when doc_upload_thread triggers recalculation of index and then chat_engine, it awaits an event to be triggered on this side in order to continue receiving doc uploads
        # response = chat_engines[chat_id - 1].chat(prompt)
        response = chat_engines[1].chat(prompt)
        
        print(response)
        
def new_doc(return_event):
    global indices, chat_engines, chat_engine_functions
    indices[1] = doc_upload(indices[1], ['new information yayyyyyyyyyyyy'], ['identifier1'])
    indices[1].storage_context.persist("index")
    print('Recalculating chat engines...')
    chat_engines[1] = chat_engine_functions[1](indices[1])
    
    return_event.clear()
    print('Complete')
        
def doc_upload_thread(event, return_event):
    while True:
        time.sleep(10)
        event.set()
        return_event.wait()

def interrupt_thread(interrupt_event):
    time.sleep(100)
    interrupt_event.set()
    
def worker():
    pass

if __name__ == '__main__':  
    interrupt_event = threading.Event()
    interrupt = threading.Thread(target=interrupt_thread, args=(interrupt_event,), daemon=True)
    controller(interrupt_event)