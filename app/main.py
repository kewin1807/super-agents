# app/main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import logging

from .config import settings
# Import crew functions (adjust path if necessary)
from app.agents.crew import run_crew  # Use the function that handles input

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI CrewAI Boilerplate",
    description="API for interacting with CrewAI agents.",
    version="0.1.0",
)

client = None
db = None


@app.on_event("startup")
async def startup_db_client():
    global client, db
    try:
        logger.info(
            f"Attempting to connect to MongoDB at: {settings.mongo_uri}")
        client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        db_name = settings.mongo_uri.split(
            '/')[-1].split('?')[0]  # Extract db name
        db = client[db_name]
        logger.info(
            f"Successfully connected to MongoDB! Database: '{db_name}'")

    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        client = None  # Ensure client is None if connection fails
        db = None


@app.on_event("shutdown")
async def shutdown_db_client():
    global client
    if client:
        logger.info("Closing MongoDB connection.")
        client.close()


@app.get("/")
async def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the FastAPI CrewAI API!"}


@app.get("/health")
async def health_check():
    """Health check endpoint, including DB status."""
    db_status = "connected" if client and db else "disconnected"
    try:
        # Optional: Perform a quick read/ping to be more certain
        if client:
            client.admin.command('ping')  # Cheap command
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database_status": db_status
    }


# --- CrewAI Interaction Endpoint ---
class CrewInput(BaseModel):
    topic: str  # Define the input structure for the crew


@app.post("/run-crew")
async def trigger_crew_run(crew_input: CrewInput):
    """
    Endpoint to trigger the CrewAI crew with a specific topic.
    """
    if not settings.openai_api_key and not os.environ.get("OPENAI_API_KEY"):
        logger.warning(
            "OPENAI_API_KEY not found in environment. CrewAI might fail if using OpenAI LLM.")
        # raise HTTPException(status_code=500, detail="LLM API key not configured.")

    logger.info(f"Received request to run crew for topic: {crew_input.topic}")
    try:
        # Make sure run_crew is designed to be called like this
        result = run_crew(crew_input.topic)
        logger.info("Crew execution finished.")
        return {"result": result}
    except Exception as e:
        # Log traceback
        logger.error(f"Error running crew: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An error occurred during crew execution: {str(e)}")

# --- Example MongoDB Interaction Endpoint (Optional) ---


class Item(BaseModel):
    name: str
    description: str | None = None


@app.post("/items/")
async def create_item(item: Item):
    """Example endpoint to add an item to MongoDB."""
    if not db:
        raise HTTPException(
            status_code=503, detail="Database service unavailable")
    try:
        item_dict = item.model_dump()
        result = db.items.insert_one(item_dict)  # Assuming 'items' collection
        return {"message": "Item created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Failed to insert item into MongoDB: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to create item in database")


@app.get("/items/")
async def get_items():
    """Example endpoint to retrieve items from MongoDB."""
    if not db:
        raise HTTPException(
            status_code=503, detail="Database service unavailable")
    try:
        # Exclude MongoDB's _id field
        items_cursor = db.items.find({}, {"_id": 0})
        items = list(items_cursor)
        return items
    except Exception as e:
        logger.error(f"Failed to retrieve items from MongoDB: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve items from database")


# Placeholder for Gradio app mounting (if needed and running in the same process)
# from .gradio_app import create_gradio_interface # Assuming you have gradio_app.py
# gradio_app = create_gradio_interface()
# app = gr.mount_gradio_app(app, gradio_app, path="/gradio") # Mount Gradio on /gradio
