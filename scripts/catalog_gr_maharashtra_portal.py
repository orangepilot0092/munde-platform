"""
Catalog GR Maharashtra Portal as CRITICAL cross-domain dataset.
Sprint 34 — Data Atlas Expansion
Per 03_DATA_ATLAS_AND_RESEARCH.md: Dataset Metadata Standard + AI Readiness Assessment
Uses os.environ directly to avoid settings module caching localhost DB URL.
"""

import os
import psycopg2
from psycopg2.extras import Json

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

metadata = Json(
    {
        "resource_id": "gr_maharashtra_portal",
        "dataset_name": "Maharashtra Government Resolutions (GR Portal)",
        "domain": "Cross-Domain",
        "secondary_domains": [
            "Agriculture",
            "Water",
            "Energy",
            "Urban",
            "Industry",
            "Environment",
            "Disaster",
            "Land",
            "Transport",
            "Citizen Services",
        ],
        "department": "General Administration Department (GAD)",
        "source": "gr.maharashtra.gov.in",
        "license": "Government Open Data License (GODL)",
        "refresh_frequency": "Daily",
        "total_records_current": 535,
        "format": "PDF",
        "priority": "critical",
        "schema_fields": [
            "SN",
            "Department_Name",
            "Title",
            "Unique_Code",
            "GR_Date",
            "File_Size_KB",
            "Download_URL",
        ],
        "data_snapshot": {
            "latest_date": "2026-07-09",
            "departments_represented": [
                "Agriculture",
                "Co-operation",
                "Skill Development",
                "Finance",
                "Food & Civil Supplies",
                "General Administration",
            ],
            "key_schemes_identified": [
                "Punyashlok Ahilyadevi Holkar Farmers Loan Waiver 2026",
                "Special Assistance to States for Capital Investment",
                "7th Pay Commission ITI Staff",
            ],
        },
        "ai_readiness": [
            "RAG Context for Policy Q&A",
            "Scheme Eligibility Classification",
            "Entity Extraction (Departments, Officers, Locations)",
            "Temporal Policy Change Detection",
            "Cross-Department Correlation Analysis",
            "Agent Grounding for All 10 Setus",
        ],
        "quality_scores": {
            "freshness": 5,
            "completeness": 4,
            "accuracy": 5,
            "machine_readability": 3,
            "authority": 5,
            "overall": 4.4,
        },
        "processing_requirements": {
            "ocr_needed": True,
            "marathi_nlp": True,
            "entity_extraction": True,
            "vector_embedding": True,
        },
        "kg_entities": ["GR", "Department", "Scheme", "Officer", "District", "Policy"],
        "kg_relationships": [
            "gr_issued_by_department",
            "gr_establishes_scheme",
            "gr_appoints_officer",
            "gr_amends_policy",
            "scheme_benefits_district",
        ],
        "cross_domain_mapping": {
            "krishisetu": [
                "Loan Waiver",
                "Cocoon Market",
                "Animal Husbandry Transfers",
            ],
            "urjasetu": ["Capital Investment Assistance"],
            "nagarsestu": ["Building Layout Plans", "ITI Infrastructure"],
            "jansestu": [
                "Pay Commission",
                "Ex-Servicemen Welfare",
                "Appointing Authority",
            ],
            "udyogsetu": ["Cocoon Processing Center", "Capital Investment"],
        },
        "verified_date": "2026-07-10",
    }
)

cur.execute(
    """
    INSERT INTO metadata_registry (dataset_id, name, domain, source_url, metadata)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (dataset_id) DO UPDATE SET metadata = EXCLUDED.metadata
""",
    (
        "ds_gr_maharashtra_portal",
        "Maharashtra Government Resolutions (GR Portal)",
        "Cross-Domain",
        "https://gr.maharashtra.gov.in",
        metadata,
    ),
)

conn.commit()
cur.close()
conn.close()
print("✅ Cataloged GR Maharashtra Portal as CRITICAL cross-domain dataset")
