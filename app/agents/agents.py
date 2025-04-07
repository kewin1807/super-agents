# app/agents/agents.py
from crewai import Agent
from app.config import settings
import os

# Set up environment variable for CrewAI (if needed, e.g., for OpenAI)
# Ensure the API key is available in the environment where the app runs
# os.environ["OPENAI_API_KEY"] = settings.openai_api_key or "DEFAULT_KEY_IF_NONE"

# Define your agents here
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and data science',
    backstory="""You work at a leading tech think tank.
        Your expertise lies in identifying emerging trends.
        You have a knack for dissecting complex data and presenting
        actionable insights.""",
    verbose=True,
    allow_delegation=False,
    # You can pass llm=your_llm_instance here if using a specific model
    # llm=ollama_llm # Example for Ollama
)

writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="""You are a renowned Content Strategist, known for
        your insightful and engaging articles.
        You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True
)

# Add more agents as needed
