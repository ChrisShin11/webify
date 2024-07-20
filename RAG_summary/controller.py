from env import ROOT_DIR
from index import get_doc_index
import os
from llama_index.llms.together import TogetherLLM
from llama_index.core.memory import ChatMemoryBuffer

def init():
    
    try:
        llm = TogetherLLM(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo", api_key=os.environ['TOGETHER_API_KEY']
        )   
        return llm 
    except Exception as e:
        print('Error loading model: '+ str(e))

def rag_global_summary_chat(llm, overwrite_index=False):

    index = get_doc_index(llm, overwrite_index=overwrite_index)
    query_engine = index.as_query_engine(
        response_mode='tree_summarize', use_async=True
    )
    
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
    
    
    
def rag_singular_doc_context(llm, doc):
    pass

#orchestration should possible work on a higher level? same with llm init
#graph information necessary (relationships) vs document information
def orchestrate_tasks():
    pass 

def controller():
    pass
        
if __name__ == '__main__':  
    print('Nothing')