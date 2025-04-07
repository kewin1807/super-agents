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
