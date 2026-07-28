"""
Project Munde — Vector Search
Semantic search using pgvector cosine similarity.
"""
from typing import List, Dict
import psycopg2
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer
import structlog

logger = structlog.get_logger(__name__)

# Load embedding model once (cached)
_embedding_model = None

def _get_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        logger.info("loading_embedding_model", model="all-MiniLM-L6-v2")
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model

def _get_db_connection():
    """Get a connection to the PostgreSQL database with pgvector"""
    return psycopg2.connect(
        host="192.168.29.20",
        port=5432,
        database="munde_core",
        user="munde",
        password="munde_dev_password"
    )

async def search_similar(query: str, top_k: int = 3) -> List[Dict]:
    """
    Search for similar intelligence assets using semantic similarity.
    
    Args:
        query: The search query (will be embedded)
        top_k: Number of results to return
    
    Returns:
        List of dicts with keys: name, description, similarity_score, domain
    """
    try:
        # 1. Generate embedding for the query
        model = _get_model()
        query_embedding = model.encode(query).tolist()
        
        # 2. Query pgvector for similar documents
        conn = _get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Use pgvector cosine distance operator (<=>)
                # Convert distance to similarity: 1 - distance
                sql = """
                    SELECT 
                        name,
                        description,
                        domain,
                        1 - (embedding <=> %s::vector) AS similarity_score
                    FROM intelligence_assets
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """
                cur.execute(sql, (query_embedding, query_embedding, top_k))
                results = cur.fetchall()
                
                # Convert to list of dicts
                return [
                    {
                        "name": r["name"],
                        "description": r["description"],
                        "domain": r["domain"],
                        "similarity_score": float(r["similarity_score"])
                    }
                    for r in results
                ]
        finally:
            conn.close()
            
    except Exception as e:
        logger.error("vector_search_failed", error=str(e), query=query[:100])
        return []
