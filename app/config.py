# app/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    mongo_uri: str = os.getenv(
        "MONGO_URI", "mongodb://localhost:27017/mydatabase")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    # Add other configurations as needed

    class Config:
        # If you don't use .env file, pydantic can read directly from environment variables
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'  # Ignore extra fields from environment


# Create a single instance of the settings
settings = Settings()

# Example usage (optional, just for demonstration)
if __name__ == "__main__":
    print(f"Mongo URI: {settings.mongo_uri}")
    print(f"OpenAI Key loaded: {bool(settings.openai_api_key)}")
