# app/agents/tasks.py
from crewai import Task
from .agents import researcher, writer  # Import your defined agents

# Define your tasks here
task1 = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
      Identify key trends, breakthrough technologies, and potential industry impacts.
      Your final answer MUST be a full analysis report""",
    expected_output='A comprehensive full analysis report on the latest AI advancements.',
    agent=researcher  # Assign task to the researcher agent
)

task2 = Task(
    description="""Using the insights provided by the researcher, develop an engaging blog
      post that highlights the most significant AI advancements.
      Your post should be informative yet accessible, catering to a tech-savvy audience.
      Make it sound cool, avoid complex words so it doesn't sound like AI.
      Your final answer MUST be the full blog post of at least 4 paragraphs.""",
    expected_output='A 4-paragraph blog post on significant AI advancements.',
    agent=writer  # Assign task to the writer agent
)
