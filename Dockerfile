# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies (if any)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

# Set the working directory in the container
WORKDIR /app

# Copy only files necessary for dependency installation first to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
# --no-root: Don't install the project itself as editable, just dependencies
# --no-dev: Exclude development dependencies in the final image
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY ./app /app/app
# Copy .env file if needed inside the container (ensure it doesn't contain secrets for public images)
# COPY .env /app/.env

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
# Use --host 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]