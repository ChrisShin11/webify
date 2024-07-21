from llama_index.core import Document
from llama_index.core.memory import ChatMemoryBuffer

##need to test     
def doc_upload(index, text_chunks, identifiers):
    
    doc_chunks = []
    for i, text in enumerate(text_chunks):
        doc = Document(text=text, id = str(identifiers[i]))
        doc_chunks.append(doc)
        
    for chunk in doc_chunks:
        index.insert(chunk)
        
    return index

#make async
def get_rag_doc_summary_chat(index, memory=None):
    
    if memory == None:
        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    
    chat_engine = index.as_chat_engine(
        chat_mode ='context',
        memory=memory,
        system_prompt=("""You are a chatbot, provided with unstructured data 
            regarding a set of many employees and their current projects.
            If a question is very general, try to answer through reference to a variety of the unstructured data you have available.
            You are able to answer specific questions regarding these employees and projects, and should 
            provide in depth explanations of technologies referenced, but only when asked to. Explanations should be abstract for non technical stakeholders and minute for technical stakeholders. 
            You should inquire at what technical depth level the user is most comfortable.
            If they are technical or otherwise experience in their field, do not go into detail on simple or common concepts / roles.
            You should initially ask what the user would like to know about the company.""",
        ),
    )
    
    return chat_engine

#vector embedding
def graph_insert(llm, new_entities):
    pass

def get_rag_graph_chat(index, memory=None):
    if memory == None:
        memory = ChatMemoryBuffer.from_defaults(token_limit=8192)
        
    chat_engine = index.as_chat_engine(
        chat_mode = 'context',
        memory=memory,
        system_prompt=("""You are a chatbot provided with relational data, originally in graph form. 
                       It will follow a schema PERSON: [WORKS_ON, WORKS_WITH, WORKS_AS, WORKS_FOR], TASK: [ASSIGNED_TO, ASSOCIATED_WITH], 
                       DEPARTMENT: [ASSOCIATED_WITH, WORKS_ON], 
                       POSITION: [ASSOCIATED_WITH, ASSIGNED_TO], PROJECT: [ASSIGNED_TO, ASSOCIATED_WITH]
                       Answer relation-based questions over this data. 
                       You may be asked to enumerate Entities. Pleae provide a list in this case."""),
    )
    
    
    return chat_engine
    
    