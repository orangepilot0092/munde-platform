"""
End-to-End RAG Agent Demo for Project Sahyadri.
Takes a natural language query, finds relevant datasets via semantic search,
fetches real data from PostGIS, and generates a cited natural language answer.
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
OLLAMA_GENERATE_URL = f"http://{AI_NODE_IP}:11434/api/generate"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = (
    "qwen2.5:14b"  # Or qwen2, mistral, etc., depending on what's pulled on your AI Node
)


async def get_ollama_embedding(text: str) -> List[float]:
    payload = {"model": EMBEDDING_MODEL, "prompt": text}
    async with httpx.AsyncClient(timeout=30.0) as client:
        logger.info(f"Generate URL: {OLLAMA_GENERATE_URL}")
        logger.info(f"Model: {LLM_MODEL}")
        logger.info(f"Payload: {payload}")
        response = await client.post(OLLAMA_EMBED_URL, json=payload)
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        response.raise_for_status()
        return response.json().get("embedding", [])


async def generate_llm_response(prompt: str) -> str:
    payload = {"model": LLM_MODEL, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=120.0) as client:
        logger.info(f"Generate URL: {OLLAMA_GENERATE_URL}")
        logger.info(f"Model: {LLM_MODEL}")
        logger.info(f"Payload: {payload}")
        response = await client.post(OLLAMA_GENERATE_URL, json=payload)
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        response.raise_for_status()
        return response.json().get("response", "No response generated.")


async def fetch_data_for_dataset(conn, dataset_id: str, location: str = "Pune") -> str:
    """Fetch sample data based on the dataset ID."""
    if "weather" in dataset_id or "rainfall" in dataset_id or "power" in dataset_id:
        query = """
            SELECT date, precipitation_mm, temp_max_c, temp_min_c 
            FROM atlas.maharashtra_weather_daily 
            WHERE district_name ILIKE $1 
            ORDER BY date DESC 
            LIMIT 5;
        """
        rows = await conn.fetch(query, f"%{location}%")
        if rows:
            return "Recent Weather Data:\n" + "\n".join(
                [
                    f"  - {r['date']}: Rain={r['precipitation_mm']}mm, Max={r['temp_max_c']}°C, Min={r['temp_min_c']}°C"
                    for r in rows
                ]
            )
        return "No recent weather data found for this location."

    elif "biodiversity" in dataset_id or "gbif" in dataset_id:
        # Approximate Pune coords: 73.8567, 18.5204. 0.5 degrees is roughly 50km radius
        query = """
            SELECT species_name, common_name, occurrence_date 
            FROM atlas.maharashtra_biodiversity_occurrences 
            WHERE ST_DWithin(geometry, ST_SetSRID(ST_MakePoint(73.8567, 18.5204), 4326), 0.5)
            ORDER BY occurrence_date DESC NULLS LAST
            LIMIT 5;
        """
        rows = await conn.fetch(query)
        if rows:
            return "Recent Biodiversity/Pest Observations near Pune:\n" + "\n".join(
                [
                    f"  - {r['species_name']} ({r['common_name'] or 'Unknown'}) observed on {r['occurrence_date']}"
                    for r in rows
                ]
            )
        return "No recent biodiversity observations found near this location."

    elif "rivers" in dataset_id:
        query = "SELECT DISTINCT name, waterway_type FROM atlas.maharashtra_rivers WHERE waterway_type = 'river' LIMIT 5;"
        rows = await conn.fetch(query)
        if rows:
            return "Major Rivers in Maharashtra:\n" + "\n".join(
                [f"  - {r['name']}" for r in rows]
            )
        return "No river data found."

    return "Dataset recognized, but specific data fetching logic not yet implemented for this demo."


async def run_rag_agent(query: str):
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    logger.info(f"🤖 RAG Agent Query: '{query}'")

    try:
        conn = await asyncpg.connect(
            user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
        )

        # 1. Semantic Search
        logger.info("🔍 Step 1: Semantic Search for relevant datasets...")
        query_vector = await get_ollama_embedding(query)
        vector_str = f"[{','.join(map(str, query_vector))}]"

        search_sql = """
            SELECT dataset_id, name, description, 1 - (embedding <=> CAST($1 AS vector)) AS similarity
            FROM sahyadri.metadata_registry
            WHERE embedding IS NOT NULL
            ORDER BY similarity DESC
            LIMIT 2;
        """
        datasets = await conn.fetch(search_sql, vector_str)

        context_data = []
        for ds in datasets:
            logger.info(
                f"   ✅ Found: {ds['name']} (Similarity: {ds['similarity']:.2f})"
            )

            # 2. Fetch Real Data
            logger.info(f"   📥 Fetching sample data from {ds['dataset_id']}...")
            data = await fetch_data_for_dataset(conn, ds["dataset_id"], location="Pune")
            context_data.append(f"DATASET: {ds['name']}\nDATA:\n{data}\n")

        # 3. LLM Generation
        logger.info("🧠 Step 3: Generating cited response via LLM...")
        system_prompt = """You are an AI assistant for Project Sahyadri, a geospatial intelligence platform for Maharashtra.
Answer the user's query accurately using ONLY the provided context data. 
If the data doesn't contain the answer, state that clearly. 
Always cite the specific dataset name when mentioning facts.
Format your response clearly with bullet points."""

        user_prompt = f"Query: {query}\n\nContext Data:\n" + "\n---\n".join(
            context_data
        )
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = await generate_llm_response(full_prompt)

        print("\n" + "=" * 80)
        print("📊 RAG AGENT RESPONSE")
        print("=" * 80)
        print(response)
        print("=" * 80 + "\n")

    except Exception as e:
        logger.error(f"❌ RAG Agent failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if "conn" in locals():
            await conn.close()


async def main():
    test_queries = [
        "What was the recent rainfall and temperature in Pune district?",
        "Are there any reported agricultural pests or biodiversity observations near Pune?",
        "Tell me about the major rivers in Maharashtra and recent weather patterns.",
    ]

    for q in test_queries:
        await run_rag_agent(q)


if __name__ == "__main__":
    asyncio.run(main())
