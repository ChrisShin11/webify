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

4. Run the application using Docker Compose:

```bash
docker-compose up --build
```

5. OR, Run the fastapi application using uvicorn:

```bash
uvicorn main:app --reload
```

6. OR, Run the fastapi development server:
    
```bash
fastapi dev
```

This command will build the Docker image and start the container. The API will be accessible at `http://localhost:4070`.

## Directory Structure after Setup

```plaintext
csvembed/
├── .venv/
│   └── ...
├── app/
│   ├── models/
│   │   ├── csv_models.py
│   │   └── embedding_models.py
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── data/
│   ├── invalid_columns.csv
│   ├── missing_response.csv
│   └── valid.csv
├── tests/
│   ├── __init__.py
│   ├── test_csv_endpoint.py
│   └── test_embedding_endpoint.py
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
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

# Task 5 - Questions

**1. Suppose you needed to secure your API so it can be accessed by a Front-End Application - what sort of Security/Auth would you consider adding? What about making it accessible to an analytics pipeline on a remote server?**
    
To secure the API for access by a front-end application, I very much like to use a good implementtion of server managed Token Authentication (example [django-rest-knox](https://github.com/jazzband/django-rest-knox)) because of the following reasons that I find useful very often:
- unlike JWT, implementation of multi-device authentication and session management is easier.
- it is easier to revoke tokens.
- easier implementation of token expiration.

Other well known methods of securing the API for access are obviously:
- OAuth2.0 and
- JWT (JSON Web Tokens).

Other necessary steps for Security in Production:
- HTTPS (TLS/SSL)
- Proper CORS (Cross-Origin Resource Sharing) configuration to restrict access to specific domains for the frontends.

For making the API accessible to an analytics pipeline on a remote server, I would:
- Use role-based API keys or access tokens to authenticate the remote server.
- Implement rate limiting and throttling to prevent abuse and ensure fair usage incase we need to give other parties access to this API, atleast the stand rate limit feature from FastAPI.
- We can also opt for AWS's VPS only access or even using VPN or IP whitelisting to restrict access to the API although API keys are recommended to also accompany this.

**2. You are told you need to store the contents of uploaded user files in a database. What type of Database would you use and why?**

If we want the user to be in control of their files as well as its management, I would opt to store the user uploaded files as is in a cloud storage service like AWS S3 or Google Cloud Storage. 

If we just need to store the contents of the uploaded files in a known way, I would store the contents in a NoSQL database like MongoDB or a SQL database like PostgreSQL, depending on the use case.

For an extension to this task, we can use a document-oriented database like MongoDB. MongoDB is known as go to for storing unstructured or semi-structured data, such as CSV files and good horizontal scaling capabilities.

**3. Now consider having to store users’ text and embeddings. What type of database would you use for that? Could this and the uploaded file data be stored in the same database? Why might you want/not want to do this?**

For storing users' text and embeddings, I would use a vector db. Vector DBs are optimized for storing and querying high-dimensional vectors/embeddings. My top choices: Chroma DB, Elasticsearch and TypeSense (relatevely new project but I like it personally). Elasticsearch and TypeSense are search engines first but can be used to store embeddings as well allowing for advanced integration with search capabilities.

It is possible to store both the uploaded file data and the text embeddings in the same primary database (relational or non-relational either), but it is more efficient to use a dedicated vector database for storing them, if that is a priority.

Simply put, storing them separately allows for keeping and handling those two tasks as independent tasks, such that scaling and optimization of each type can be applied easily based on their specific requirements.

**4. Consider the Embedding model you used for your API route. What factors might affect the type of embedding model you select if they were to be stored for search later?**

I'll consider the following factors that come to mind:
    
- Dimensionality of the embeddings: The dimensionality of the embeddings affects the accuracy, performance and requirements. Higher-dimensional embeddings provide more accurate representations but require more storage space and computational resources for search operations.

- Inference time: The model's inference time is necessary to be considered, especially if real-time search is required. Smaller and faster models may be preferred for low-latency search scenarios but we might sacrifice accuracy for it.

- The language and domain: The embedding model should be suitable for the domain and language of the text data being processed. Models pre-trained on specific domains (literature, medical field, engineering, programming, etc.) or languages (English, Mandarin, French, multi-lingual, etc.) provide better results for those applications, so this is also an important factor.

- Similarity measure available or not: The choice of similarity measure (e.g., cosine similarity, Euclidean distance) used for comparing embeddings should support with the characteristics of the embedding model.
        
**5. What text editor and color theme do you currently use?**

VS Code with Tokyo Night theme ❤️ (was a gruvbox fan previously).

**6. What is your favourite Python package and why?**

Django with Django Rest Framework (popular web-framework in Python). Familiarity I guess. I like the way Django is structured the way it is and yes the _bulkiness_ of it is sometimes noticible but I guess the monolith approach of it grew on me over several projects.

Solid Runner-ups:
    
- [Sanic](https://sanic.dev/en/): a fast asynchronous Python web framework - I know it looks and sounds very memey but I assure you it gets the job done and fast. Built several home projects with it and use it regularly. Main upside for me is it is all batteries included, production server too, no need for gunicorn or uvicorn. Super fast and no brainer websocket and file streaming support.

- [pywinauto](https://github.com/pywinauto/pywinauto): Windows GUI automation library - I got to know how dynamic attributes (aka magic attributes) can be implemented and used in Python. Also I got to learn how to build a wrapper library looking and working with this package in one of my previous jobs.

**7. What new features do you think GPT 4.5/5 will have when it releases?**

Haha, might be a easier question to answer seeing as to how GPT-4o was just announced this week (the voice synthesis sound awesome btw).
As to answer the question, I future versions of GPT, as well as other LLMs are likely to move towards what GPT-4o has claimed right now: go from being multi-modal to do-everything-in-same-model-because-that-is-what-seems-to-be-working-right-now approach. Because why optimize 3 models for an auto-dubbing pipeline when you can just use one model to do all the work.

Other features I think it should have are:
- come equipped with vector database capabilities to store and retrieve information. Long term memory and longer context lengths.
- more context awareness
- better understanding of the context and the user's intent
- if we're looking at conversational chatbots, some sort of mechanism to mimic or fully simulate personality would be nice (chatbots quickly become boring after 10 something messages on same topic).
- support for non-given context or current running knowledge? don't know what to call this. e.g. know if today is Mother's Day when I ask why are flowers so expensive today.