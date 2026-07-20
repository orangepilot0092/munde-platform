import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from psycopg2.extras import Json
from src.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()

metadata = Json(
    {
        "resource_id": "TO_BE_EXTRACTED_FROM_API_TAB",
        "dataset_name": "Maharashtra Monthly Energy Supply-Demand Balance (Apr 2021 - Feb 2025)",
        "domain": "Energy",
        "department": "Ministry of Power / CEA",
        "source": "Data.gov.in",
        "license": "Government Open Data License (GODL)",
        "refresh_frequency": "Monthly",
        "last_updated": "2025-02-28",
        "temporal_coverage": "2021-04 to 2025-02 (47 months)",
        "geographic_resolution": "State-level aggregate",
        "priority": "critical",
        "schema_fields": [
            "Month",
            "Energy_Requirement_MU",
            "Energy_Supplied_MU",
            "Energy_Not_Supplied_MU",
            "Energy_Deficit_Pct",
            "Peak_Demand_MW",
            "Peak_Met_MW",
            "Peak_Not_Met_MW",
            "Peak_Deficit_Pct",
        ],
        "data_snapshot": {
            "months_covered": 47,
            "zero_deficit_months": 35,
            "worst_peak_deficit": {"month": "Sep-24", "mw": 3506, "pct": 11.7},
            "peak_demand_range_mw": {"min": 21141, "max": 30151},
            "energy_requirement_range_mu": {"min": 12704, "max": 18766},
            "deficit_season_pattern": "Aug-Sep recurring; Apr secondary peak",
            "demand_growth_cagr_pct": 4.3,
        },
        "ai_readiness": [
            "Monthly Load Forecasting (Prophet/LSTM)",
            "Peak Deficit Early Warning System",
            "Seasonal Pattern Classification",
            "Anomaly Detection (Unusual deficit months)",
            "Capacity Expansion Planning Support",
            "RAG Context for Energy Policy Queries",
        ],
        "quality_scores": {
            "freshness": 5,
            "completeness": 5,
            "accuracy": 5,
            "machine_readability": 5,
            "temporal_resolution": 5,
            "overall": 5.0,
        },
        "urjasetu_mapping": {
            "use_cases": [
                "Real-time energy deficit dashboard",
                "Seasonal load shedding prediction",
                "Grid reliability scorecard",
                "Renewable integration gap analysis",
                "Industrial power availability advisory",
            ],
            "alert_triggers": {
                "warning": "Peak deficit > 5%",
                "critical": "Peak deficit > 10%",
                "emergency": "Energy deficit > 1%",
            },
        },
        "verified_date": "2026-07-09",
    }
)

cur.execute(
    """
    INSERT INTO metadata_registry (dataset_id, name, domain, source_url, metadata)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (dataset_id) DO UPDATE SET metadata = EXCLUDED.metadata
""",
    (
        "ds_energy_balance_monthly_mh",
        "MH Monthly Energy Balance (2021-25)",
        "Energy",
        "https://data.gov.in/apis",
        metadata,
    ),
)

conn.commit()
cur.close()
conn.close()
print("✅ Cataloged Energy Balance MH as CRITICAL priority for UrjaSetu")
