# ADR-0004: Adoption of Dagster for Idempotent, Lineage-Tracked ETL Pipelines

* **Status:** Proposed
* **Date:** 2026-07-15
* **Deciders:** Engineering Leadership, Data Platform Team
* **Context:** 
  During Sprints 30–37, we successfully proved the concept of data ingestion using ad-hoc Python scripts (e.g., NASA POWER, Geofabrik, GBIF). However, scaling to the target of 300–500 official datasets requires a production-grade orchestration framework. Ad-hoc scripts lack built-in idempotency, automated lineage tracking, dependency management, and observability.

* **Decision:** 
  We will adopt **Dagster** as the primary ETL orchestration framework for Project Sahyadri. All data ingestion, transformation, and validation workflows must be modeled as Dagster `@asset`s or `@op`s. 

* **Consequences:**
  * **Positive:** 
    * Built-in data lineage and dependency graphs.
    * Idempotent execution (safe to re-run).
    * Native integration with our Metadata Registry and Quality Framework.
    * Excellent observability via Dagster UI, exportable to Prometheus/Grafana.
  * **Negative:** 
    * Requires refactoring existing ad-hoc scripts into Dagster assets.
    * Slight learning curve for developers new to Dagster's asset-based paradigm.

* **Compliance:** 
  Aligns with Engineering Constitution: *Data First, Idempotency, Lineage, Observability*.
