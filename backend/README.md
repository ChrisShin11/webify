# Webify

team:

Date: 2024-05-18

---

Basic Description:

# Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Directory Structure after Setup](#directory-structure-after-setup)
- [API Endpoints](#api-endpoints)
    - [POST /csv](#post-csv)
    - [GET /embedding](#get-embedding)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)
- [Task 5 - Questions](#task-5---questions)

## Requirements

- Python 3.11+
- Docker
- Docker Compose

## Setup

1. Clone the repository (private repository) or extract it from the zip file provided. Navigate to the project directory:

```bash
git clone https://github.com/{url} # optional
cd webify
```
2. Create and activate the virtual environment:

```bash
python -m venv .venv

$ source .venv/bin/activate # Linux/macOS
# or
> .venv\Scripts\activate # Windows
```

3. Install the Python dependencies:

```bash
pip install -r requirements.txt
```
4. Edit file within the python virtual env

Delete or comment the following line of code in python-env\Lib\site-packages\llama_index\core\indices\knowledge_graph\base.py
```
269                 self._graph_store.upsert_triplet(*triplet)
```

5. Run the application using Docker Compose:

```bash
docker-compose up --build
```

6. OR, Run the fastapi application using uvicorn:

```bash
uvicorn main:app --reload
```

7. OR, Run the fastapi development server:
    
```bash
fastapi dev
```

This command will build the Docker image and start the container. The API will be accessible at `http://localhost:4070`.

## Directory Structure after Setup

```plaintext
webify/
├── backend/
│   ├── app/
│   │   └── ...
│   ├── tests/
│   │   └── ...
│   ├── .dockerignore
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── README.md
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── docs/
│   │   ├── csv_models.py
│   │   └── embedding_models.py
│   ├── public/
│   │   └── ...
│   ├── src/
│   │   └── ...
│   └── utils.py
├── neo4j-llama3-integration/
│   ├── data/
│   │   └── ...
│   ├── graph_constructor.py
│   ├── trained_document_files.txt
│   ├── graph_query.py
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── RAG_summary/
│   ├── data/
│   │   └── ...
│   ├── chat_engine.py
│   ├── controller.py
│   ├── env.py
│   ├── index.py
│   ├── helper.py
│   └── tasks.json
├── index
│   └── ...
├── storage
│   ├── index_store.json
│   └── ...
├── .gitignore
└── README.md
```

## API Endpoints

### POST /csv

- Description: Accepts a CSV file and an optional "equals" query parameter, and returns the rows in the CSV where the "Value" column matches the "equals" value as JSON.
- Request:
    - File: CSV file (required)
    - Query Parameter: "equals" (optional)
- Response: JSON array of rows matching the "equals" value

### GET /embedding

- Description: Accepts a "text" query parameter and returns a JSON object containing a text embedding.
- Request:
    - Query Parameter: "text" (required)
- Response: JSON object with the "embedding" key containing the text embedding

This will run all the tests defined in the `tests` directory.

## API Documentation

The API documentation is automatically generated using Swagger UI. You can access the interactive documentation by navigating to `http://localhost:4070/docs` in your web browser after running the container or the application.

The Swagger UI provides a user-friendly interface to explore and test the API endpoints. It displays information about each endpoint, including the request and response formats, required parameters, and example requests and responses.

You can use the Swagger UI to send requests to the API endpoints and test them directly from the documentation page and view the corresponding responses.

## Multi-Agent RAG Workflow

Webify manages and leverages both rigid graph structures as well as unstructured document objects in order to model a richer image of employees and their working environment. In order to answer dynamic queries over both data types, we implemented the Multi-Agent RAG Workflow using LLamaIndex. We instantiated two separate chat engines with shared chat memory, and one independent agent to discern whether Agent 1 (RAG over Graph) or Agent 2 (RAG over Documents) was better suited to answer the question.

### Orchestration

The specific query used to discern between Agents is the following:

```
    response = llm.complete(f"""Given the following task descriptions, and the following prompt, please output only a 1 or a 2 corresponding to the closest matching task.
                            Prompt: {prompt}. Task Descriptions: {tasks}. Do not output anything other than a 1 or 2.""")
```
and in ```RAG_summary/tasks.json```, you can find the following:

```
[
    {
        "task_id": "1",
        "task_name": "Graph Relation Question",
        "description": "Output solely '1' if the query you were provided is explicitly inquiring into the following relationships over two or more of the provided entities: PERSON: [WORKS_ON, WORKS_WITH, WORKS_AS, WORKS_FOR], TASK: [ASSIGNED_TO, ASSOCIATED_WITH], DEPARTMENT: [ASSOCIATED_WITH, WORKS_ON], POSITION: [ASSOCIATED_WITH, ASSIGNED_TO], PROJECT: [ASSIGNED_TO, ASSOCIATED_WITH]. Also Output '1' if the query is asking about entity counts or enumeration of entities."
    },
    {
        "task_id": "2",
        "task_name": "General RAG over documents",
        "description": "Output solely '2' if the query you were provided is not inquiring into the provided relations."
    }
]
```

The origin of the referenced schema can be seen when discussing our Neo4j Integration.

Generally, we see that Agent 1 is given control over the response flow when the user asks for enumerations or inquires into relationships over our employees. This data can be enriched and the schema altered as necessary for the relationships / aggregate understandings needed of the entity graph at any given company.

When the orchestrator is unsure, we defer to Agent 2, for the more classical Document Summary RAG flow.

### Iterative Indexing

Webify provides a platform for employees to asyncronously upload their documents with confidence that their work will contribute to the model of their shared workspace. We use event-triggers to maintain consistency with uploaded documents, seamlessly iterating on the indices and re-generating the chat engines. 

Our controller module keeps both chats rendered at all times, and maintains chat logs. When our orchestrator switches response flow between agents, the agent being rotated in will be provided the chat history, such that no change is perceived by the user.

### Module Specification

LLama3 was the LLM used for each of the above agents. Agent 1 uses a KnowledgeGraphIndex and Agent 2 runs off of a DocumentSummaryIndex.

## Neo4j Integration

The file named "graph_constructor.py" contains two integral functions for creating and accessing the neo4j graph store from the provided documentation. 

### constructs_nodes_from_documents_init()

This function uses an llm to create neo4j graph nodes based on input documentation, in our usecase this documentation is related to company organization and project information. 

#### Graph Structure

Entities and relationships are hardcoded assuming that organizations will have similar needs, therefore allowing the work to be done by the developers rather than the end user. In the future, we can integrate user input to change these for niche use cases. The following were used in the context of this project:

    Entities: PERSON, TASK, DEPARTMENT, POSITION, PROJECT

    Relations: WORKS_WITH, WORKS_AS, WORKS_FOR, SUPERVISES, SUPERVISED BY, ASSIGNED_TO, ASSOCIATED_WITH

A validation schema relating which relationships can be assigned to which entities needs to be derived from the given entities and relations. For now it is hardcoded to the following: 

    PERSON:     ASSIGNED_TO, WORKS_WITH, WORKS_AS, SUPERVISES, SUPERVISED BY
    TASK:       ASSIGNED_TO, ASSOCIATED_WITH
    DEPARTMENT: ASSOCIATED_WITH, ASSIGNED_TO
    POSITION:   ASSOCIATED_WITH, ASSIGNED_TO"
    PROJECT:    ASSIGNED_TO, ASSOCIATED_WITH
    
#### Input Data Extraction

By default, the llm will stricly follow this validation schema along with the given entities and relations. This ensures that the graph data that is being generated by the LLM does not hallucinate obscure realtions that are outside of the scope of what information we want to be extracted from the input documentation. By setting the kg_extractors 'strict' parameter to false, we can allow values outside of the schema. This will decrease percision of graph data but increase the overall information extracted from the input documentation.

The input files are tracked through the "trained_document_files.txt" file, indicating whether an input data file in the data directory has already been used to generate graph nodes.

All files that are being seen for the first time are passed along with the kg_extractor, that has the graph structure and llm, to the PropertyGraphIndex.from_documents(_args_) function from llama-index-core for the creation of the neo4j graph. Upon the completion of the function call, the neo4j database is updated with the generated graph nodes along with their relationships.

### index_from_neo4j_graph()

The index_from_neo4j_graph() function is used to store the index vector embeddings in the ./storage directory. The file of interest within this directory is the index_store.json. This function loads a hardcoded neo4j Cypher query as a document and passes it to llama-index-core's KnowledgeGraphIndex.from_documents(_args_) function along with the graph store itself which is passed in within the storage_context variable. This function uses the query to recieve the approriate graph nodes and stores their embeddings in ./storage/index_store.json file mentioned above. 

## Running Tests

To run the unit tests, execute the following command:

```bash
pytest
```
A total of 6 tests are defined in two test files as outlined in Task 2 - Unit Testing.

## Troubleshooting

If you encounter any issues while setting up or running the application, please ensure that:

- This project was tested on a Windows 10 machine. Suggested to run on a Windows 10 machine.
- You have the required dependencies installed.
- The CSV files in the `data` directory are properly formatted.
- Docker and Docker Compose are installed and running correctly.

If the issue persists, please do contact me via [email](mailto:patel.nishils@northeastern.edu).
