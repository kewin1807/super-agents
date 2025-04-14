import asyncio
import os
import time
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import SseServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_ext.agents.file_surfer import FileSurfer
from autogen_ext.agents.magentic_one import MagenticOneCoderAgent
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from dotenv import load_dotenv
load_dotenv()


async def main() -> None:
    # Create server params for the remote MCP service
    server_params = SseServerParams(
        url="http://localhost:8002/sse",
        timeout=120,  # Connection timeout in seconds
    )
    tools = await mcp_server_tools(server_params)

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    mcpAssistant = AssistantAgent(
        name="Analyst",
        model_client=model_client,
        tools=tools,
        system_message=f"""
        You are financial analyst. You are given a financial statement and you need to analyze it and provide a report about VN stock (you can use fireant.vn to get the latest news and information about VN stock).
        """
    )
    coder = MagenticOneCoderAgent(
        "coder",
        model_client=model_client,
    )

    writer = AssistantAgent(
        "save_report",
        model_client=model_client,
        system_message=f"""
        You are a writer. You are given a report and you need to save it to a markdown file.
        """
    )

    team = MagenticOneGroupChat(
        participants=[mcpAssistant, coder, writer],
        model_client=model_client,
    )
    start_time = time.time()

    # Let the agent translate some text
    await Console(
        team.run_stream(task=f"""Analyze the financial statement and provide a report of TCB VN STOCK. Run until the report is saved to a markdown file.
                         - Please analyze the financial statement and provide a report of one ticker that you want.
        - Analyze the price and volume of the ticker from (2025-03-01) to (2025-04-13) and combine with some indicators such as RSI, MACD, Bollinger Bands, etc.
        - Research how much foreign investors have bought
        - Analyze the news about the ticker (posts, sentiment, etc.)
        - Give a comprehensive report and conclusion about the ticker and give me a recommendation to buy or sell and entry for short term.
        - Create a workspace directory on the root of the project and write the report to a markdown file.
                        """,
                        cancellation_token=CancellationToken())
    )
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main())
