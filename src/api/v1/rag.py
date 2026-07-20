from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.rag_context import RAGContextAssembler
from src.core.llm import LLMService

router = APIRouter(prefix="/rag", tags=["RAG & Intelligence"])


@router.get("/context")
def assemble_rag_context(
    query: str = Query(...),
    district: str = Query("Solapur"),
    entity: str = Query("Sugarcane"),
    db: Session = Depends(get_db),
):
    assembler = RAGContextAssembler(db)
    return assembler.assemble_context(query, district, entity)


@router.get("/chat")
def rag_chat(
    query: str = Query(..., description="The user's natural language question"),
    district: str = Query(
        "Solapur", description="Target district for geospatial context"
    ),
    entity: str = Query(
        "Sugarcane", description="Target entity for knowledge graph context"
    ),
    db: Session = Depends(get_db),
):
    """
    Full RAG Execution Pipeline (Sprint 32).
    1. Assembles multi-domain context (PC Node).
    2. Sends context + query to LLM (AI Node).
    3. Returns the final generated answer.
    """
    # Step 1: Assemble Context (Sprint 31)
    assembler = RAGContextAssembler(db)
    context = assembler.assemble_context(query, district, entity)

    # Step 2: Generate Answer via AI Node (Sprint 32)
    llm = LLMService()
    answer = llm.generate_response(context["system_prompt"], query)

    return {
        "query": query,
        "answer": answer,
        "context_used": {
            "policies_retrieved": context["retrieved_policies"],
            "kg_facts": context["knowledge_graph_facts"],
            "geospatial_data": context["geospatial_data"],
        },
    }
