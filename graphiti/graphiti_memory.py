from graphiti_core import Graphiti
# from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
# from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from datetime import datetime
import time
from graphiti_core.llm_client.anthropic_client import AnthropicClient

from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
import os
import logging
import asyncio
import json
from graphiti_core.utils.bulk_utils import RawEpisode
from graphiti_core.nodes import EpisodeType
from graphiti_core.utils.maintenance.graph_data_operations import clear_data
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF
from app.config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

llm_client = OpenAIClient(
    config=LLMConfig(
        api_key=settings.openai_api_key,
        model="gpt-4o"
    )
)

# llm_client = AnthropicClient(
#     cache=False,
#     config=LLMConfig(
#         api_key=settings.anthropic_api_key,
#         model="claude-3-5-sonnet-latest"
#     )
# )

# embedder = OpenAIEmbedder(
#     config=OpenAIEmbedderConfig(
#         api_key=settings.openai_api_key,
#         embedding_model="text-embedding-3-small"
#     )
# )

graphiti = Graphiti(
    os.environ.get("NEO4J_URI"),
    os.environ.get("NEO4J_USER"),
    os.environ.get("NEO4J_PASSWORD"),
    llm_client=llm_client,
)


async def add_episodes():
    await clear_data(graphiti.driver)
    await graphiti.build_indices_and_constraints()

    wallet = 'FTg1gqW7vPm4kdU1LPM7JJnizbgPdRDy2PitKw6mY27j'
    # read json file with relative path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "data.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    print(data[0])
    start_time = time.time()
    for i, episode in enumerate(data):
        print(f"Adding episode {i} of {len(data)}")
        start_time_episode = time.time()
        await graphiti.add_episode(
            name=f"Transaction {i} of {wallet}",
            source_description=f"Metadata for transaction {i} of {wallet}. That includes the transaction hash, the timestamp, the amount, the sender, the receiver, source, routers and more information.",
            source=EpisodeType.json,
            episode_body=str({k: v for k, v in episode.items()}),
            reference_time=datetime.fromtimestamp(episode["Time"]),
            group_id=wallet
        )
        end_time_episode = time.time()
        print(
            f"Time taken for episode {i}: {end_time_episode - start_time_episode}s")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}s")
    # start_time_batch = time.time()

    # bulk_episodes = [
    #     RawEpisode(
    #         name=f"Transaction {i} of {wallet}",
    #         source_description=f"Metadata for transaction {i} of {wallet}. That includes the transaction hash, the timestamp, the amount, the sender, the receiver, source, routers and more information.",
    #         source=EpisodeType.json,
    #         content=str({k: v for k, v in episode.items()}),
    #         reference_time=datetime.fromtimestamp(episode["Time"]),
    #     )
    #     for i, episode in enumerate(data)
    # ]
    # await graphiti.add_episode_bulk(bulk_episodes)
    # print(f"Added {len(bulk_episodes)} episodes")
    # end_time_batch = time.time()
    # print(f"Time taken for batch: {end_time_batch - start_time_batch}s")
    print("Done")


async def search_query(query: str, num_results: int = 10):
    # config for search, we have many config search recipes
    # node_search_config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
    # node_search_config.limit = 10

    results = await graphiti.search(query, num_results=num_results)
    if len(results) > 0:
        for result in results:
            print(f'UUID: {result.uuid}')
            print(f'Fact: {result.fact}')
            print(f'Valid from: {result.valid_at}')
            print(f'Invalid until: {result.invalid_at}')
        print('---')

if __name__ == "__main__":
    print("Adding episodes")
    asyncio.run(add_episodes())
    print("Searching")
    asyncio.run(search_query(
        "Give me information of the number of token transferred in the wallet", num_results=5))
