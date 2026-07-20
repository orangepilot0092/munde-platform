# ADR-0001: Choice of PostgreSQL + pgvector for Vector Storage

## Status
Accepted

## Context
Project Sahyadri requires a high-performance vector database to store and query embeddings for the RAG (Retrieval-Augmented Generation) pipeline. We evaluated dedicated vector databases (Qdrant, Pinecone, Milvus) against PostgreSQL with the `pgvector` extension.

## Decision
We have decided to use **PostgreSQL 16 with the `pgvector` extension** as our primary vector store and relational database.

## Consequences
### Pros
1. **Operational Simplicity:** Maintaining a single database engine for both relational data (metadata, users, audit logs) and vector embeddings drastically reduces operational overhead.
2. **ACID Compliance:** Vector updates and metadata updates can occur in a single transaction, ensuring data consistency.
3. **No Data Egress/Sync Issues:** Eliminates the need to keep a separate vector DB in sync with the primary relational DB.
4. **Mature Ecosystem:** PostgreSQL's tooling (backups, monitoring, extensions like PostGIS) is enterprise-grade.

### Cons
1. **Scale Limits:** For extremely massive vector datasets (billions of vectors), dedicated vector DBs might offer better raw throughput. However, for Sahyadri's initial scale, pgvector with HNSW indexing is more than sufficient.

## Compliance
This decision aligns with the Sahyadri Engineering Principle: *"Simplicity over cleverness"* and *"Reuse before rewrite"*.
