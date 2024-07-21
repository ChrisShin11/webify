from env import ROOT_DIR
from index import get_doc_index, get_graph_index
from helper import read_json_from_file
from chat_engine import get_rag_doc_summary_chat, doc_upload, get_rag_graph_chat
import os
import json
from llama_index.core import Settings
# from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM

import threading
import time

indices = [None, None]
index_storage = ['graph_index', 'index']
chat_engine_functions = [get_rag_graph_chat, get_rag_doc_summary_chat]
chat_engines = [None, None]

def init():
    
    try:
        llm = TogetherLLM(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo", api_key=os.environ['TOGETHER_API_KEY']
        )   
        
        Settings.llm = llm
        # Settings.embed_model = TogetherEmbedding(model_name="togethercomputer/m2-bert-80M-8k-retrieval",
        #                 api_key=os.environ['TOGETHER_API_KEY'])
        
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
    global indices, chat_engines
    
    llm = init()
    
    graph_index = get_graph_index()
    rag_doc_index = get_doc_index(llm, overwrite_index=False)
    
    indices = [graph_index, rag_doc_index]    ## handling index here allows us to re-compute indices with respect to thread coordination
    
    chat_engines = [chat_engine_functions[0](indices[0]), chat_engine_functions[1](indices[1])]
    
    api_event = threading.Event()
    return_event = threading.Event()
    
    #create threads - in reality I believe we will have three threads managed by the API, so this definition will have to be removed from here
    api_thread = threading.Thread(target=doc_upload_thread, args=(api_event, return_event), daemon=True)
    
    api_thread.start()
    custom_chat_history = []
    
    last_id = None
    
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
        
        # maintain ChatMessage List of all interactions, regenerate chat_engine when swapping 
        response = chat_engines[chat_id - 1].chat(prompt)
        # response = chat_engines[1].chat(prompt)
        
        print(response)
        
def new_doc(return_event):
    global indices, chat_engines
    #updates for graph will be pushed in from neo4j side?
    for i in range(1,2):    
        indices[i] = doc_upload(indices[i], ['new information yayyyyyyyyyyyy'], ['identifier1'])
        indices[i].storage_context.persist(index_storage[i])
        print('Recalculating chat engines...')
        chat_engines[i] = chat_engine_functions[i](indices[i])
    
    return_event.clear()
    print('Complete')
        
def doc_upload_thread(event, return_event):
    while True:
        time.sleep(20)
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