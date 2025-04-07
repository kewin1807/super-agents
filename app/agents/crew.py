# app/agents/crew.py
from crewai import Crew, Process
from .agents import researcher, writer  # Import your agents
from .tasks import task1, task2  # Import your tasks


def create_crew():
    """Creates and returns the CrewAI crew."""
    return Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=2,  # You can set it to 1 or 2 to different logging levels
        # Sequential process is default, but explicitly defined here
        process=Process.sequential
        # memory=True # Enable memory for the crew
        # You can add more configurations like manager_llm, memory, cache, etc.
    )

# You could also define a function to run the crew with specific inputs


def run_crew(topic: str):
    """
    Initializes and runs the crew for a given topic.
    Note: This example modifies the task descriptions based on the input topic.
    Adjust this logic based on how you want your crew to handle dynamic inputs.
    """
    # Dynamically adjust task descriptions if needed (example)
    task1.description = f"""Conduct a comprehensive analysis of the latest advancements in {topic}.
        Identify key trends, breakthrough technologies, and potential industry impacts.
        Your final answer MUST be a full analysis report"""

    task2.description = f"""Using the insights provided, develop an engaging blog post
        about {topic}. Highlight the most significant advancements.
        Your post should be informative yet accessible.
        Make it sound cool, avoid complex words.
        Your final answer MUST be the full blog post of at least 4 paragraphs."""

    # Recreate or update the crew if tasks have changed significantly
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=2,
        process=Process.sequential
    )

    result = crew.kickoff()
    return result


# Example usage (for testing this module directly)
if __name__ == "__main__":
    print("Initializing Crew...")
    # Simple kickoff without dynamic input
    # simple_crew = create_crew()
    # result = simple_crew.kickoff()
    # print("\n\nCrew Result:")
    # print(result)

    # Kickoff with dynamic input
    topic_input = "Quantum Computing breakthroughs in 2024"
    print(f"\nRunning Crew for topic: {topic_input}")
    dynamic_result = run_crew(topic_input)
    print("\n\nDynamic Crew Result:")
    print(dynamic_result)
