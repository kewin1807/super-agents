from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters
from google.adk.tools import google_search
from google.adk.runners import Runner
import streamlit as st
import logging
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = "Financial Analyst"
USER_ID = "default_user"
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")


class FinancialAnalystAgent:
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.runner = None
        self.coordinator_agent = None

    async def get_mcp_tools(self):
        tools, exit_stack = await MCPToolset.from_server(
            connection_params=SseServerParams(
                url="http://localhost:8002/sse")
        )
        return tools, exit_stack

    async def initial_technical_analysis(self, tools):
        return LlmAgent(
            name="Technical_Analyst",
            model="gemini-2.0-flash-exp",
            instruction="""
            You are a financial analyst. You are good at technical analysis.
            You are given a stock symbol and you need to analyze the technical analysis of a stock.
            You should get OHLC data of the stock from fireant_tools and apply some indicators to analyze the stock.
            Also, you can search by built-in google search search function to get more information OHLC data stock.
            Should get tools the relevant to OHLC data.
            """,
            description="Analyze the technical analysis of a stock",
            output_key="technical_analysis",
            tools=tools,
        )

    async def initial_fundamental_analysis(self, tools):
        return LlmAgent(
            name="Fundamental_Analyst",
            model="gemini-2.0-flash-exp",
            instruction="""
            You are an financial expert. You are good at fundamental analysis and macro analysis.
            You are given a stock symbol and you need to analyze the fundamental analysis of a stock.
            You should find the fundamental data of the stock from fireant_tools, get relevant blog or post about the stock from tools and google search.
            Also, you can search by built-in google search search function to get more information fundamental data stock.
            Should get tools the relevant to fundamental data.
            """,
            description="Analyze the fundamental analysis of a stock",
            tools=tools,
            output_key="fundamental_analysis",
        )

    async def initial_sentiment_analysis(self, tools):
        return LlmAgent(
            name="Sentiment_Analyst",
            model="gemini-2.0-flash-exp",
            instruction="""
            You are an financial expert. You are good at sentiment analysis.
            You are given a stock symbol and you need to analyze the sentiment analysis of a stock.
            You should find the sentiment data of the stock from fireant_tools, get relevant blog or post about the stock from tools and google search.
            Also, you can search by built-in google search search function to get more information sentiment data stock.
            Should get tools the relevant to sentiment data.
            """,
            description="Analyze the sentiment analysis of a stock",
            output_key="sentiment_analysis",
            tools=tools,
        )

    async def init_writer(self):
        return LlmAgent(
            name="Report_Writer",
            model="gemini-2.0-flash-exp",
            instruction="""
            You are a financial analyst. You are good at writing reports.
            You are given a stock symbol and you need to write a report about the stock.
            Give me the comprehensive report about the stock, include:
            - Technical analysis
            - Fundamental analysis
            - Sentiment analysis
            - Macro analysis
            - Any other relevant information
            """,
            description="Write a report about the stock",
            output_key="report",
        )

    async def coordinator(self):
        # tools, _ = await self.get_mcp_tools()
        technical_analysis = await self.initial_technical_analysis([google_search])
        fundamental_analysis = await self.initial_fundamental_analysis([google_search])
        sentiment_analysis = await self.initial_sentiment_analysis([google_search])
        writer = await self.init_writer()

        self.coordinator_agent = SequentialAgent(
            name="Financial_Analyst",
            description="Coordinates specialized finance agents to provide comprehensive financial advice",
            sub_agents=[
                technical_analysis,
                fundamental_analysis,
                sentiment_analysis,
                writer,
            ]
        )
        self.runner = Runner(
            agent=self.coordinator_agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )

    async def run(self, query):
        session_id = f"finance_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            self.session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
            )
            user_content = types.Content(
                role='user',
                parts=[types.Part(text=query)]
            )

            async for event in self.runner.run_async(user_id=USER_ID,
                                                     session_id=session_id,
                                                     new_message=user_content):
                if event.is_final_response() and event.author == self.coordinator_agent.name:
                    break
            updated_session = self.session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id
            )
            result = {}
            keys = ["report"]
            for key in keys:
                value = updated_session.state.get(key)
                result[key] = value
                print(f"Update session {key}: {value}")
                return result
        except Exception as e:
            logger.exception(f"Error during finance analysis: {str(e)}")
            raise
        finally:
            self.session_service.delete_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id
            )


async def main():

    st.set_page_config(
        page_title="Financial Analyst",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
    )

    with st.sidebar:
        st.title("Financial Analyst")
        st.caption(
            "This application uses Google's ADK (Agent Development Kit) and Gemini AI to provide personalized financial advice.")
        st.info("📝 Please ensure you have your Gemini API key in the .env file:\n```\nGOOGLE_API_KEY=your_api_key_here\n```")

    container = st.container()
    with container:
        st.title("Analyze Stock")
        query = st.text_input("Enter the stock symbol you want to analyze")
        if st.button("Analyze"):
            st.write(f"Analyzing {query}...")

    st.divider()
    finance_system = FinancialAnalystAgent()
    await finance_system.coordinator()

    if query:
        result = await finance_system.run(query)
        for key, value in result.items():
            st.markdown(f"### {key}")
            st.markdown(value)


if __name__ == "__main__":
    asyncio.run(main())
