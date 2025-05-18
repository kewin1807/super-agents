# FastAPI CrewAI MongoDB Boilerplate

This is a boilerplate project for creating a FastAPI application that integrates with CrewAI agents and uses MongoDB as a database, all containerized using Docker Compose.

## Features

-   **FastAPI**: Modern, fast (high-performance) web framework for building APIs.
-   **CrewAI**: Framework for orchestrating role-playing, autonomous AI agents.
-   **MongoDB**: NoSQL database for storing application data.
-   **Poetry**: Dependency management.
-   **Docker & Docker Compose**: Containerization for easy setup and deployment.
-   **Configuration Management**: Uses `.env` file and Pydantic settings.
-   **Basic API Endpoints**: Root, health check, CrewAI interaction, and example MongoDB CRUD.

## Prerequisites

-   Docker ([https://www.docker.com/get-started](https://www.docker.com/get-started))
-   Docker Compose (usually included with Docker Desktop)
-   Poetry ([https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)) (Optional, for local development without Docker)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Configure Environment Variables:**
    -   Rename `.env.example` to `.env` (or create `.env` from scratch).
    -   Update the variables inside `.env`, especially:
        -   `MONGO_URI`: Keep the default `mongodb://mongo:27017/mydatabase` if running via Docker Compose. Change `mydatabase` if needed.
        -   `OPENAI_API_KEY`: Add your OpenAI API key if your CrewAI agents require it. **Do not commit this file with your key to public repositories.**

3.  **Build and Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    -   Use the `-d` flag to run in detached mode (in the background): `docker-compose up --build -d`

4.  **Access the API:**
    -   The FastAPI application will be available at [http://localhost:8000](http://localhost:8000).
    -   You can access the Swagger UI documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
    -   The MongoDB instance will be accessible on `localhost:27017` from your host machine (useful for GUI clients like MongoDB Compass).

## Running Locally (Without Docker)

1.  **Install Dependencies:**
    ```bash
    poetry install
    ```

2.  **Run MongoDB:**
    -   You'll need a local MongoDB instance running. You can install it directly or run it via Docker separately:
        ```bash
        docker run -d -p 27017:27017 --name local-mongo mongo:latest
        ```
    -   Update `MONGO_URI` in your `.env` file to `mongodb://localhost:27017/mydatabase`.

3.  **Run the FastAPI App:**
    ```bash
    poetry run uvicorn app.main:app --reload --port 8000
    ```
    The application will be available at [http://localhost:8000](http://localhost:8000).

## Project Structure


## LightRag
We can start the lightRag/main.py to understand all the process from input data and retrieval, or we can use ```source .env lightrag-server``` to start webui

Here is env example when we use lightrag
```
# # .env
# MONGO_URI="mongodb://mongo:27017/mydatabase" # Use service name 'mongo' from docker-compose
# OPENAI_API_KEY= # Replace with your actual key if needed by CrewAI agents
# ANTHROPIC_API_KEY=

NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD=""



# LLM_BINDING=openai
# LLM_MODEL=gpt-4o
# LLM_BINDING_HOST=https://api.openai.com/v1
# LLM_BINDING_API_KEY=
# ### Max tokens sent to LLM (less than model context size)

# # EMBEDDING_BINDING_API_KEY=your_api_key

# NEO4J_URI="neo4j://localhost:7687"
# NEO4J_USERNAME="neo4j"
# NEO4J_PASSWORD=""
OPENAI_API_KEY=


# ### Server Configuration
# # HOST=0.0.0.0
# PORT=9621
# WORKERS=2

# ### Settings for document indexing
# ENABLE_LLM_CACHE_FOR_EXTRACT=true
# SUMMARY_LANGUAGE=English
# MAX_PARALLEL_INSERT=2

# ### LLM Configuration (Use valid host. For local services installed with docker, you can use host.docker.internal)
# TIMEOUT=200
# TEMPERATURE=0.0
# MAX_ASYNC=4
# MAX_TOKENS=32768

# ### Embedding Configuration (Use valid host. For local services installed with docker, you can use host.docker.internal)
# EMBEDDING_BINDING=openai
# EMBEDDING_BINDING_HOST=https://api.openai.com/v1
# EMBEDDING_MODEL=text-embedding-3-small
# EMBEDDING_DIM=1024



### This is sample file of .env


### Server Configuration
HOST=0.0.0.0
PORT=9621
WEBUI_TITLE='My Graph KB'
WEBUI_DESCRIPTION="Simple and Fast Graph Based RAG System"
OLLAMA_EMULATING_MODEL_TAG=latest
# WORKERS=2
# CORS_ORIGINS=http://localhost:3000,http://localhost:8080

### Login Configuration
# AUTH_ACCOUNTS='admin:admin123,user1:pass456'
# TOKEN_SECRET=Your-Key-For-LightRAG-API-Server
# TOKEN_EXPIRE_HOURS=48
# GUEST_TOKEN_EXPIRE_HOURS=24
# JWT_ALGORITHM=HS256

### API-Key to access LightRAG Server API
# LIGHTRAG_API_KEY=your-secure-api-key-here
# WHITELIST_PATHS=/health,/api/*

### Optional SSL Configuration
# SSL=true
# SSL_CERTFILE=/path/to/cert.pem
# SSL_KEYFILE=/path/to/key.pem

### Directory Configuration (defaults to current working directory)
### Should not be set if deploy by docker (Set by Dockerfile instead of .env)
### Default value is ./inputs and ./rag_storage
# INPUT_DIR=<absolute_path_for_doc_input_dir>
# WORKING_DIR=<absolute_path_for_working_dir>

### Max nodes return from grap retrieval
# MAX_GRAPH_NODES=1000

### Logging level
# LOG_LEVEL=INFO
# VERBOSE=False
# LOG_MAX_BYTES=10485760
# LOG_BACKUP_COUNT=5
### Logfile location (defaults to current working directory)
# LOG_DIR=/path/to/log/directory

### Settings for RAG query
# HISTORY_TURNS=3
# COSINE_THRESHOLD=0.2
# TOP_K=60
# MAX_TOKEN_TEXT_CHUNK=4000
# MAX_TOKEN_RELATION_DESC=4000
# MAX_TOKEN_ENTITY_DESC=4000

### Entity and ralation summarization configuration
### Language: English, Chinese, French, German ...
SUMMARY_LANGUAGE=English
### Number of duplicated entities/edges to trigger LLM re-summary on merge ( at least 3 is recommented)
# FORCE_LLM_SUMMARY_ON_MERGE=6
### Max tokens for entity/relations description after merge
# MAX_TOKEN_SUMMARY=500

### Number of parallel processing documents(Less than MAX_ASYNC/2 is recommended)
# MAX_PARALLEL_INSERT=2
### Chunk size for document splitting, 500~1500 is recommended
# CHUNK_SIZE=1200
# CHUNK_OVERLAP_SIZE=100

### LLM Configuration
ENABLE_LLM_CACHE=true
ENABLE_LLM_CACHE_FOR_EXTRACT=true
### Time out in seconds for LLM, None for infinite timeout
TIMEOUT=240
### Some models like o1-mini require temperature to be set to 1
TEMPERATURE=0
### Max concurrency requests of LLM
MAX_ASYNC=4
### MAX_TOKENS: max tokens send to LLM for entity relation summaries (less than context size of the model)
### MAX_TOKENS: set as num_ctx option for Ollama by API Server
MAX_TOKENS=32768
### LLM Binding type: openai, ollama, lollms, azure_openai
LLM_BINDING=openai
LLM_MODEL=gpt-4o
LLM_BINDING_HOST=https://api.openai.com/v1
LLM_BINDING_API_KEY=
### Optional for Azure
# AZURE_OPENAI_API_VERSION=2024-08-01-preview
# AZURE_OPENAI_DEPLOYMENT=gpt-4o

### Embedding Configuration
### Embedding Binding type: openai, ollama, lollms, azure_openai
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIM=1536
EMBEDDING_BINDING_API_KEY=
# If the embedding service is deployed within the same Docker stack, use host.docker.internal instead of localhost
EMBEDDING_BINDING_HOST=https://api.openai.com/v1
### Num of chunks send to Embedding in single request
# EMBEDDING_BATCH_NUM=32
### Max concurrency requests for Embedding
# EMBEDDING_FUNC_MAX_ASYNC=16
### Maximum tokens sent to Embedding for each chunk (no longer in use?)
# MAX_EMBED_TOKENS=8192
### Optional for Azure
# AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
# AZURE_EMBEDDING_API_VERSION=2023-05-15

### Data storage selection
# LIGHTRAG_KV_STORAGE=PGKVStorage
# LIGHTRAG_VECTOR_STORAGE=PGVectorStorage
# LIGHTRAG_DOC_STATUS_STORAGE=PGDocStatusStorage
# LIGHTRAG_GRAPH_STORAGE=Neo4JStorage

### TiDB Configuration (Deprecated)
# TIDB_HOST=localhost
# TIDB_PORT=4000
# TIDB_USER=your_username
# TIDB_PASSWORD='your_password'
# TIDB_DATABASE=your_database
### separating all data from difference Lightrag instances(deprecating)
# TIDB_WORKSPACE=default

### PostgreSQL Configuration
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=postgres
# POSTGRES_DATABASE=lightrag
# POSTGRES_MAX_CONNECTIONS=12
### separating all data from difference Lightrag instances(deprecating)
# POSTGRES_WORKSPACE=default

### Neo4j Configuration
NEO4J_URI="neo4j://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="Cuongnh1807@"
LIGHTRAG_GRAPH_STORAGE=Neo4JStorage

LIGHTRAG_VECTOR_STORAGE=MilvusVectorDBStorage
### Independent AGM Configuration(not for AMG embedded in PostreSQL)
# AGE_POSTGRES_DB=
# AGE_POSTGRES_USER=
# AGE_POSTGRES_PASSWORD=
# AGE_POSTGRES_HOST=
# AGE_POSTGRES_PORT=8529

# AGE Graph Name(apply to PostgreSQL and independent AGM)
### AGE_GRAPH_NAME is precated
# AGE_GRAPH_NAME=lightrag

### MongoDB Configuration
# MONGO_URI=mongodb://root:root@localhost:27017/
# MONGO_DATABASE=LightRAG
### separating all data from difference Lightrag instances(deprecating)
# MONGODB_GRAPH=false

### Milvus Configuration
MILVUS_URI=http://localhost:19530
MILVUS_DB_NAME=default

MILVUS_USER=
MILVUS_PASSWORD=
MILVUS_TOKEN="root:Milvus"
# MILVUS_TOKEN=your_token

### Qdrant
# QDRANT_URL=http://localhost:16333
# QDRANT_API_KEY=your-api-key

### Redis
REDIS_URI=redis://localhost:6379
```