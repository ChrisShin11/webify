# from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper
import os
from neo4j import GraphDatabase
from app.config import settings

class DocumentProcessor:
    def __init__(self):
        self.neo4j_driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

    # async def process_document(self, file_path: str):
    #     # Load the document
    #     documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        
    #     # Create an index from the documents
    #     index = GPTVectorStoreIndex.from_documents(documents)
        
    #     # Extract relevant information (this is a simplified example)
    #     query_engine = index.as_query_engine()
    #     employee_info = query_engine.query("Extract all employee information from this document.")
        
    #     # Update Neo4j with the extracted information
    #     self._update_neo4j(employee_info)

    # def _update_neo4j(self, employee_info):
    #     with self.neo4j_driver.session() as session:
    #         # This is a simplified example. You'd need to parse the employee_info
    #         # and create appropriate Cypher queries based on the extracted data.
    #         session.run("""
    #             MERGE (e:Employee {name: $name})
    #             SET e.position = $position,
    #                 e.department = $department
    #         """, name=employee_info.name, position=employee_info.position, department=employee_info.department)

document_processor = DocumentProcessor()