"""
Test semantic search across the Intelligence Asset Registry using pgvector.
"""

import asyncio
import logging
import os
import httpx
from typing import List

try:
    import asyncpg
except ImportError:
    print("❌ asyncpg not found. Install via: poetry add asyncpg")
    exit(1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

AI_NODE_IP = os.getenv("AI_NODE_IP", "192.168.29.96")
OLLAMA_EMBED_URL = f"http://{AI_NODE_IP}:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"


async def get_ollama_embedding(text: str) -> List[float]:
    """Fetch embedding from local Ollama instance."""
    payload = {"model": EMBEDDING_MODEL, "prompt": text}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(OLLAMA_EMBED_URL, json=payload)
        response.raise_for_status()
        return response.json().get("embedding", [])


async def test_semantic_search(query: str, limit: int = 3):
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    logger.info(f"🔍 Semantic Search Query: '{query}'")

    try:
        conn = await asyncpg.connect(
            user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
        )

        # 1. Embed the query
        logger.info("🧠 Generating query embedding...")
        query_vector = await get_ollama_embedding(query)
        vector_str = f"[{','.join(map(str, query_vector))}]"

        # 2. Search metadata_registry using pgvector cosine distance (<=>)
        # 1 - (embedding <=> query) gives cosine similarity (1.0 = perfect match)
        search_sql = """
            SELECT 
                dataset_id, 
                name, 
                domain,
                description,
                1 - (embedding <=> CAST($1 AS vector)) AS similarity_score
            FROM sahyadri.metadata_registry
            WHERE embedding IS NOT NULL
            ORDER BY similarity_score DESC
            LIMIT $2;
        """

        results = await conn.fetch(search_sql, vector_str, limit)

        logger.info("\n" + "=" * 80)
        logger.info("📊 SEMANTIC SEARCH RESULTS")
        logger.info("=" * 80)

        for i, row in enumerate(results, 1):
            logger.info(f"Rank #{i} | Similarity: {row['similarity_score']:.4f}")
            logger.info(f"  🆔 Dataset ID : {row['dataset_id']}")
            logger.info(f"  📛 Name       : {row['name']}")
            logger.info(f"  🏛️  Domain     : {row['domain']}")
            logger.info(
                f"  📝 Description: {(row['description'] or 'No description available')[:100]}..."
            )
            logger.info("-" * 80)

    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
    finally:
        if "conn" in locals():
            await conn.close()


async def main():
    # Test queries relevant to Project Sahyadri use cases
    queries = [
        "I need data about rainfall and weather patterns in Pune district for farming.",
        "Show me datasets related to air pollution and health in urban areas.",
        "Find information about water reservoir levels and groundwater in Maharashtra.",
    ]

    for q in queries:
        await test_semantic_search(q, limit=3)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
