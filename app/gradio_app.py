# app/gradio_app.py
import gradio as gr
from app.agents.crew import run_crew  # Import the function that runs the crew
import logging
import time
from dotenv import load_dotenv


logger = logging.getLogger(__name__)


def crew_chat_interface(topic, history):
    """
    Function to handle the chat interaction for the Gradio interface.
    'history' is automatically managed by Gradio ChatInterface.
    """
    logger.info(f"Gradio interface received topic: {topic}")
    try:
        # Add a thinking indicator (optional)
        yield "🤖 Thinking..."  # Using yield makes it stream-like if needed

        start_time = time.time()
        # Call the function that runs your crew
        result = run_crew(topic)  # Pass the user input as the topic
        end_time = time.time()

        logger.info(
            f"Crew finished in {end_time - start_time:.2f} seconds.")
        # Return the final result from the crew
        yield str(result)  # Ensure the output is a string

    except Exception as e:
        logger.error(f"Error in Gradio chat interface: {e}", exc_info=True)
        yield f"An error occurred: {str(e)}"


def create_gradio_interface():
    """Creates the Gradio Chat Interface."""
    # Use ChatInterface for a built-in chat UI
    chat_interface = gr.ChatInterface(
        fn=crew_chat_interface,
        title="CrewAI Agent Chat",
        description="Enter a topic for the AI crew to research and write about.",
        examples=[["Latest advancements in Renewable Energy"],
                  ["Summarize the impact of AI on healthcare"]],
        chatbot=gr.Chatbot(height=600),
        textbox=gr.Textbox(
            placeholder="Ask the crew about a topic...", container=False, scale=7),
        theme="soft",  # Or other themes like "default", "huggingface"
        submit_btn="Run Crew",
        retry_btn="Retry",
        undo_btn="Undo",
        clear_btn="Clear Chat",
    )
    return chat_interface


# To run Gradio separately (not mounted in FastAPI):
if __name__ == "__main__":
    print("Launching Gradio Interface...")
    # Ensure environment variables (like API keys) are loaded if running directly
    load_dotenv()  # Load .env from the root directory relative to this file's execution context

    interface = create_gradio_interface()
    # Launch on port 7860
    interface.launch(server_name="0.0.0.0", server_port=7860)
