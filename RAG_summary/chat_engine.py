from env import ROOT_DIR
from helper import read_json_from_file
from index import get_doc_index
import os
import json
from llama_index.core import Settings, Document
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.memory import ChatMemoryBuffer
        
def doc_upload(llm, text_chunks, identifiers):
    index = get_doc_index(llm, overwrite_index=False)
    
    doc_chunks = []
    for i, text in enumerate(text_chunks):
        doc = Document(text=text, id = str(identifiers[i]))
        doc_chunks.append(doc)
        
    for chunk in doc_chunks:
        index.insert(chunk)

#make async
def rag_doc_summary_chat(llm, overwrite_index=False):

    index = get_doc_index(llm, overwrite_index=overwrite_index)
    
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    
    chat_engine = index.as_chat_engine(
        chat_mode ='context',
        memory=memory,
        system_prompt=("""You are a chatbot, provided with graphical and unstructured data 
            regarding a set of employees and their current objectives / overall skills. 
            Only provide information on members if you are asked for it. Projects you can speak on more freely.
            You are able to answer specific questions regarding the context you are provided, and should 
            provide in depth explanations of technologies referenced, both abstractly for non technical stakeholders and minutely for technical stakeholders. 
            You should inquire at what technical depth level the user is most comfortable.
            If they are technical or otherwise experience in their field, do not go into detail on simple or common concepts / roles.""",
        ),
    )
    
    return chat_engine

#vector embedding
def graph_insert(llm, new_entities):
    pass

def rag_graph_chat(llm, doc):
    pass

#orchestration should possible work on a higher level? same with llm init
#graph information necessary (relationships) vs document information
def orchestrate_tasks(llm, prompt):
    path = os.path.join(ROOT_DIR, 'tasks.json')
    tasks = json.dumps(read_json_from_file(path), indent=4)
    
    response = llm.complete(f"""Given the following task descriptions, and the following prompt, please output only a 1 or a 2 corresponding to the closest matching task.
                            Prompt: {prompt}. Task Descriptions: {tasks}. Do not output anything other than a 1 or 2.""")
    
    return response
    