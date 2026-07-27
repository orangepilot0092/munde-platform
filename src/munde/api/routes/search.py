"""
Semantic Search API: Find relevant Intelligence Assets using local vector similarity.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from typing import List
from sentence_transformers import SentenceTransformer
import traceback

router = APIRouter(prefix="/search", tags=["Semantic Search"])

# Load the local embedding model (cached after first run)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    asset_id: str
    name: str
    description: str
    similarity_score: float

@router.post("/semantic", response_model=List[SearchResult])
async def semantic_search(request: SearchRequest):
    try:
        # 1. Generate embedding for the query locally
        query_vector = embedding_model.encode(request.query).tolist()
        
        # Convert list to string format expected by pgvector: '[0.1, 0.2, ...]'
        query_vector_str = str(query_vector)
        
        # 2. Perform vector similarity search in PostgreSQL
        db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            # Use CAST to ensure pgvector interprets the string correctly
            sql_query = text("""
                SELECT id, name, description, 
                       1 - (embedding <=> CAST(:q_vec AS vector)) as similarity
                FROM intelligence_assets
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:q_vec AS vector)
                LIMIT :top_k
            """)
            
            result = conn.execute(sql_query, {
                "q_vec": query_vector_str,
                "top_k": request.top_k
            })
            
            return [
                SearchResult(
                    asset_id=str(row.id),
                    name=row.name,
                    description=row.description or "",
                    similarity_score=round(float(row.similarity), 4)
                )
                for row in result
            ]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
