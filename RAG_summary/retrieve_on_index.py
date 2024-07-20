from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext
from llama_index.core.memory import ChatMemoryBuffer

import os

os.environ["OPENAI_API_KEY"] = 'sk-None-YooJu1Nf3u9MKjvbct01T3BlbkFJQtdfVox3UiITzuMoJaLp'
# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="index")
doc_summary_index = load_index_from_storage(storage_context)

query_engine = doc_summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)

memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

chat_engine = doc_summary_index.as_chat_engine(
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

while True:
    prompt = input('Prompt: ')
    if prompt.upper() == 'N':
        break
    
    response = chat_engine.chat(prompt)
    print(response)
