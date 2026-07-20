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
        "dataset_name": "PM-KUSUM Solar Pump Installation - District-wise Maharashtra",
        "domain": "Energy",
        "secondary_domain": "Agriculture",
        "department": "Ministry of New & Renewable Energy / MEDA",
        "source": "Data.gov.in",
        "license": "Government Open Data License (GODL)",
        "refresh_frequency": "Quarterly (estimated)",
        "geographic_resolution": "District-level (36 districts)",
        "priority": "high",
        "schema_fields": [
            "District",
            "Component_A_MW_Installed",
            "Component_B_Pumps_Installed",
            "Component_C_FLS_Pumps_Solarized",
        ],
        "data_snapshot": {
            "total_pumps_installed": 290559,
            "total_feeder_solarizations": 74674,
            "total_component_a_mw": 4,
            "top_adopter_district": {"name": "Jalna", "pumps": 29510},
            "zero_adoption_districts": [
                "Aurangabad",
                "Osmanabad",
                "Raigad",
                "Ratnagiri",
                "Sindhudurg",
            ],
            "best_feeder_integration": {"district": "Latur", "ratio_pct": 90.6},
            "component_a_gap": "Near-zero standalone solar plant deployment statewide",
        },
        "ai_readiness": [
            "District Adoption Gap Analysis",
            "Solar Irrigation Penetration Forecasting",
            "Policy Effectiveness Classification (Component A/B/C)",
            "Feeder Integration Bottleneck Detection",
            "Cross-domain RAG Context (Energy + Agriculture)",
            "Farmer Advisory Eligibility Mapping",
        ],
        "quality_scores": {
            "freshness": 4,
            "completeness": 5,
            "accuracy": 4,
            "machine_readability": 5,
            "geographic_resolution": 5,
            "overall": 4.6,
        },
        "cross_domain_mapping": {
            "urjasetu": {
                "use_cases": [
                    "Distribution company solarization planning",
                    "Feeder-level load management",
                    "Renewable energy target tracking",
                ]
            },
            "krishisetu": {
                "use_cases": [
                    "Solar pump subsidy eligibility advisory",
                    "Irrigation cost reduction estimation",
                    "District-wise adoption awareness campaigns",
                ]
            },
        },
        "kg_entities": ["District", "Solar_Pump", "Feeder", "MEDA"],
        "kg_relationships": [
            "district_has_solar_pumps",
            "feeder_solarized_under_pmkusum",
            "pmkusum_component_deployed_in",
        ],
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
        "ds_pmkusum_solar_pumps_mh",
        "PM-KUSUM Solar Pump Installation MH (District-wise)",
        "Energy",
        "https://data.gov.in/apis",
        metadata,
    ),
)

conn.commit()
cur.close()
conn.close()
print("✅ Cataloged PM-KUSUM Solar Pumps MH as HIGH priority cross-domain dataset")
