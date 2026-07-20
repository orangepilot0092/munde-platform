"""
Production FastAPI router for Knowledge Graph queries.
Supports entity lookup, relationship traversal, and natural language queries.
Aligned with Engineering Constitution: API-first, Security by Design, Explainability.
"""

import logging
import os
from typing import Any, List, Optional

import asyncpg  # type: ignore[import-untyped]
from fastapi import APIRouter, HTTPException, Query, status

from src.schemas.graph_query import (
    GraphEntityResponse,
    GraphQueryRequest,
    GraphQueryResponse,
    GraphRelationshipResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])


async def _get_graph_connection() -> asyncpg.Connection:
    """Get a dedicated asyncpg connection for graph queries."""
    return await asyncpg.connect(
        user=os.getenv("DB_USER", "sahyadri"),
        password=os.getenv("DB_PASSWORD", "sahyadri_secret"),
        database=os.getenv("DB_NAME", "sahyadri_db"),
        host=os.getenv("DB_HOST", "localhost"),
        port=5432,
    )


async def _fetch_entity(
    conn: asyncpg.Connection,
    name: str,
    entity_type: Optional[str] = None,
) -> Optional[GraphEntityResponse]:
    """Fetch a single entity by name and optional type."""
    query = """
        SELECT id, name, entity_type, properties, location_id
        FROM knowledge_graph.graph_entities
        WHERE name = $1
    """
    params: List[Any] = [name]

    if entity_type is not None:
        query += " AND entity_type = $2"
        params.append(entity_type)

    query += " LIMIT 1;"

    row = await conn.fetchrow(query, *params)
    if row is None:
        return None

    return GraphEntityResponse(
        id=row["id"],
        name=row["name"],
        entity_type=row["entity_type"],
        properties=row["properties"] if row["properties"] is not None else {},
        location_id=row["location_id"],
    )


async def _fetch_relationships(
    conn: asyncpg.Connection,
    entity_id: int,
    relationship_type: Optional[str] = None,
    limit: int = 50,
) -> List[GraphRelationshipResponse]:
    """Fetch relationships for a given entity."""
    query = """
        SELECT
            e1.id as source_id, e1.name as source_name,
            e1.entity_type as source_type, e1.properties as source_props,
            r.relationship_type,
            e2.id as target_id, e2.name as target_name,
            e2.entity_type as target_type, e2.properties as target_props
        FROM knowledge_graph.graph_relationships r
        JOIN knowledge_graph.graph_entities e1 ON r.source_id = e1.id
        JOIN knowledge_graph.graph_entities e2 ON r.target_id = e2.id
        WHERE r.source_id = $1
    """
    params: List[Any] = [entity_id]

    if relationship_type is not None:
        query += " AND r.relationship_type = $2"
        params.append(relationship_type)

    query += " LIMIT $3;"
    params.append(limit)

    rows = await conn.fetch(query, *params)

    relationships: List[GraphRelationshipResponse] = []
    for row in rows:
        source = GraphEntityResponse(
            id=row["source_id"],
            name=row["source_name"],
            entity_type=row["source_type"],
            properties=row["source_props"] if row["source_props"] is not None else {},
            location_id=None,
        )
        target = GraphEntityResponse(
            id=row["target_id"],
            name=row["target_name"],
            entity_type=row["target_type"],
            properties=row["target_props"] if row["target_props"] is not None else {},
            location_id=None,
        )
        relationships.append(
            GraphRelationshipResponse(
                source=source,
                relationship_type=row["relationship_type"],
                target=target,
            )
        )

    return relationships


@router.post(
    "/query",
    response_model=GraphQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Query the Knowledge Graph",
    description="Retrieve entities and relationships from the Knowledge Graph with citations.",
)
async def query_graph(
    request: GraphQueryRequest,
) -> GraphQueryResponse:
    """
    Query the Knowledge Graph for entities and their relationships.

    Returns:
        GraphQueryResponse with entities, relationships, citations, and confidence score.
    """
    if request.entity_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="entity_name is required for graph queries",
        )

    logger.info(
        f"Graph query: entity={request.entity_name}, "
        f"type={request.entity_type}, rel={request.relationship_type}"
    )

    conn = await _get_graph_connection()
    try:
        # 1. Fetch the target entity
        entity = await _fetch_entity(
            conn=conn,
            name=request.entity_name,
            entity_type=request.entity_type,
        )

        if entity is None:
            return GraphQueryResponse(
                entities=[],
                relationships=[],
                query_summary=f"No entity found with name '{request.entity_name}'",
                confidence_score=0.0,
                citations=[],
                metadata={"error": "entity_not_found"},
            )

        # 2. Fetch relationships
        relationships = await _fetch_relationships(
            conn=conn,
            entity_id=entity.id,
            relationship_type=request.relationship_type,
            limit=request.limit,
        )

        # 3. Collect all related entities
        related_entities: List[GraphEntityResponse] = [entity]
        for rel in relationships:
            if rel.target not in related_entities:
                related_entities.append(rel.target)

        # 4. Build citations (per AI Engineering Principles)
        citations = [
            f"knowledge_graph.graph_entities (id={entity.id})",
            f"knowledge_graph.graph_relationships (source_id={entity.id})",
        ]

        # 5. Calculate confidence score
        # Base confidence from entity existence, boosted by relationship count
        base_confidence = 0.8 if entity is not None else 0.0
        relationship_boost = min(len(relationships) * 0.02, 0.2)
        confidence_score = min(base_confidence + relationship_boost, 1.0)

        # 6. Build summary
        summary = (
            f"Found entity '{entity.name}' of type '{entity.entity_type}' "
            f"with {len(relationships)} relationships."
        )

        return GraphQueryResponse(
            entities=related_entities,
            relationships=relationships,
            query_summary=summary,
            confidence_score=round(confidence_score, 2),
            citations=citations,
            metadata={
                "query_type": "entity_lookup",
                "entity_id": entity.id,
                "relationship_count": len(relationships),
            },
        )

    except asyncpg.exceptions.UndefinedTableError:
        logger.error(
            "Knowledge graph tables do not exist. Run population pipeline first."
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Knowledge graph not yet populated. Run the population pipeline first.",
        )
    except Exception as e:
        logger.error(f"Graph query failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while querying the Knowledge Graph.",
        )
    finally:
        await conn.close()


@router.get(
    "/entities/{entity_name}",
    response_model=Optional[GraphEntityResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a single entity by name",
)
async def get_entity(
    entity_name: str,
    entity_type: Optional[str] = Query(
        None, pattern="^[a-zA-Z]+$", description="Optional entity type filter"
    ),
) -> Optional[GraphEntityResponse]:
    """Retrieve a single entity by name."""
    conn = await _get_graph_connection()
    try:
        entity = await _fetch_entity(
            conn=conn, name=entity_name, entity_type=entity_type
        )
        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entity '{entity_name}' not found",
            )
        return entity
    except asyncpg.exceptions.UndefinedTableError:
        logger.error(
            "Knowledge graph tables do not exist. Run population pipeline first."
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Knowledge graph not yet populated. Run the population pipeline first.",
        )
    except Exception as e:
        logger.error(f"Graph query failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while querying the Knowledge Graph.",
        )
    finally:
        await conn.close()
