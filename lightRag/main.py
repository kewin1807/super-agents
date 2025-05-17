import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.kg.shared_storage import initialize_pipeline_status
from dotenv import load_dotenv
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
import json
load_dotenv()

# WorkingDir
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = os.path.join(ROOT_DIR, "myKG")
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)
print(f"WorkingDir: {WORKING_DIR}")

# redis
os.environ["REDIS_URI"] = os.getenv("REDIS_URI")

# neo4j
BATCH_SIZE_NODES = 500
BATCH_SIZE_EDGES = 100
os.environ["NEO4J_URI"] = os.getenv("NEO4J_URI")
os.environ["NEO4J_USERNAME"] = os.getenv("NEO4J_USER")
os.environ["NEO4J_PASSWORD"] = os.getenv("NEO4J_PASSWORD")

# milvus
os.environ["MILVUS_URI"] = os.getenv("MILVUS_URI")
os.environ["MILVUS_USER"] = os.getenv("MILVUS_USER")
os.environ["MILVUS_PASSWORD"] = os.getenv("MILVUS_PASSWORD")
os.environ["MILVUS_DB_NAME"] = os.getenv("MILVUS_DB_NAME")
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
        kv_storage="RedisKVStorage",
        graph_storage="Neo4JStorage",
        vector_storage="MilvusVectorDBStorage",
        doc_status_storage="JsonDocStatusStorage",
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


async def main():
    # Initialize RAG instance
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "Error: OPENAI_API_KEY environment variable is not set. Please set this variable before running the program."
        )
        print("You can set the environment variable by running:")
        print("  export OPENAI_API_KEY='your-openai-api-key'")
        return  # Exit the async function

    try:
        # Clear old data files
        files_to_delete = [
            "graph_chunk_entity_relation.graphml",
            "kv_store_doc_status.json",
            "kv_store_full_docs.json",
            "kv_store_text_chunks.json",
            "vdb_chunks.json",
            "vdb_entities.json",
            "vdb_relationships.json",
        ]

        for file in files_to_delete:
            file_path = os.path.join(WORKING_DIR, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleting old file:: {file_path}")

        # Initialize RAG instance
        rag = await initialize_rag()

        # Test embedding function
        test_text = ["This is a test string for embedding."]
        embedding = await rag.embedding_func(test_text)
        embedding_dim = embedding.shape[1]
        print("\n=======================")
        print("Test embedding function")
        print("========================")
        print(f"Test dict: {test_text}")
        print(f"Detected embedding dimension: {embedding_dim}\n\n")

        with open("./data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            text = json.dumps(data)
            await rag.ainsert(text)
        query = "How many transactions are there that related to FTg1gqW7vPm4kdU1LPM7JJnizbgPdRDy2PitKw6mY27j?"
        # Perform naive search
        print("\n=====================")
        print("Query mode: naive")
        print("=====================")
        print(
            await rag.aquery(
                query, param=QueryParam(mode="naive")
            )
        )

        # Perform local search
        print("\n=====================")
        print("Query mode: local")
        print("=====================")
        print(
            await rag.aquery(
                query, param=QueryParam(mode="local")
            )
        )

        # Perform global search
        print("\n=====================")
        print("Query mode: global")
        print("=====================")
        print(
            await rag.aquery(
                query,
                param=QueryParam(mode="global"),
            )
        )

        # Perform hybrid search
        print("\n=====================")
        print("Query mode: hybrid")
        print("=====================")
        print(
            await rag.aquery(
                query,
                param=QueryParam(mode="hybrid"),
            )
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if rag:
            await rag.finalize_storages()


if __name__ == "__main__":
    asyncio.run(main())
    print("\nDone!")
