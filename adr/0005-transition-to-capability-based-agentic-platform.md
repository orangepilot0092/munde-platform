# ADR 0005: Transition to Capability-Based Agentic Platform Architecture

## Status
Accepted

## Date
2026-07-28

## Context
Project Munde began as "Project Sahyadri," a domain-specific AI assistant for Maharashtra. As the vision evolved into a general-purpose, extensible Agentic AI Platform, the existing architecture (hardcoded keyword routing, tightly coupled domain agents, and fragile HTTP-based retrieval) became a significant source of technical debt. Adding new domains or tools required rewriting core orchestration logic.

## Decision
We have refactored the core runtime to be domain-agnostic and capability-driven:

1. **Generic Agent Registry**: Introduced `AgentRegistry` where any agent (from any domain pack) can register itself and declare its `capabilities` (e.g., `["water", "reservoir", "drought"]`).
2. **Query Understanding Agent**: Replaced hardcoded keyword matching with an LLM-powered agent that extracts structured intent, entities, and required capabilities from user queries, with a robust keyword-based fallback for reliability.
3. **Domain Pack Separation**: Moved domain-specific logic (e.g., JalSetu, KrishiSetu) into a pluggable `src/munde/domain_packs/sahyadri/` directory, proving the platform can host multiple independent domains.
4. **Direct Vector Retrieval**: Replaced fragile internal HTTP calls for semantic search with direct Python imports to `pgvector`, eliminating 404 errors and reducing latency.
5. **Unified API**: Consolidated routing behind a single `/api/v1/ask` endpoint that dynamically dispatches to the appropriate agent based on extracted capabilities.

## Consequences

### Positive
- **Extensibility**: New domains, agents, and tools can be added as plugins without modifying the core orchestrator.
- **Reliability**: Robust fallbacks (both in intent detection and data retrieval) ensure the platform degrades gracefully rather than hallucinating or crashing.
- **Auditability**: Every response now includes full provenance metadata (`intent_analysis`, `routed_to`, `search_results_count`).
- **Scalability**: Sets the foundation for Phase 3 (Planner Agent) and Phase 4 (Tool Registry) to handle complex, multi-hop reasoning.

### Negative
- Slightly increased complexity in the core runtime.
- Intent parsing requires an additional LLM call (mitigated by the fast, deterministic keyword fallback).

## References
- Phase 1: Core Runtime Implementation
- Phase 2: Query Understanding Agent Implementation
- Project Munde Architectural Vision Document
