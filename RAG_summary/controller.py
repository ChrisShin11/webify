from env import ROOT_DIR
from helper import read_json_from_file
from chat_engine import get_rag_doc_summary_chat
import os
import json
from llama_index.core import Settings
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM


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
    graph_chat = None
    rag_doc_chat = get_rag_doc_summary_chat(llm)
    
    chat_engines = [graph_chat, rag_doc_chat]
    
    while True:
        prompt = input('Prompt: ')
        if prompt.upper() == 'N':
            break
        
        chat_id = choose_task_type(llm, prompt)
        
        #Use chat store to maintain the same history until reset signal()
        # response = chat_engines[chat_id - 1].chat(prompt)
        response = chat_engines[1].chat(prompt)
        
        print(response)
        
if __name__ == '__main__':  
    controller()