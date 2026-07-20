# ADR-0002: PostgreSQL + pgvector for Unified Relational and Vector Storage

## Status
Accepted

## Context
Sahyadri requires both strict relational metadata (Intelligence Assets, users, audit logs) and high-performance vector embeddings for RAG. We evaluated dedicated vector databases (Qdrant, Pinecone) against PostgreSQL with `pgvector`.

## Decision
Use **PostgreSQL 16 with the `pgvector` extension** as the single source of truth for both relational and vector data.

## Consequences
- **Pros:** Operational simplicity (one database to manage), ACID compliance for metadata+vector updates, and mature ecosystem (PostGIS for geospatial).
- **Cons:** May require careful index tuning (HNSW) at massive scale, but is more than sufficient for Phase 1-3.
