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
        "dataset_name": "Business Statistics of Crop Insurance Schemes in Maharashtra (2013-14 to 2015-16)",
        "domain": "Agriculture",
        "department": "Ministry of Agriculture and Farmers Welfare",
        "source": "Data.gov.in",
        "license": "Government Open Data License (GODL)",
        "refresh_frequency": "Historical compilation (updated 2026-02-25)",
        "last_updated": "2026-02-25",
        "temporal_coverage": "2013-14 to 2015-16",
        "geographic_resolution": "State-level aggregate",
        "priority": "high",
        "schema_fields": [
            "Year",
            "Season",
            "Scheme",
            "No_of_Farmers_Covered",
            "Area_Insured_Ha",
            "Sum_Insured_Lakh_Rs",
            "Claims_Reported_Lakh_Rs",
            "Claims_Paid_Lakh_Rs",
            "Farmers_Benefitted",
        ],
        "data_snapshot": {
            "peak_farmers_covered": 7902079,
            "peak_area_insured_ha": 5349070,
            "total_claims_paid_2014_15_lakh_rs": 193015,
            "schemes_covered": ["NAIS", "WBCIS"],
            "data_quality_flag": "2015-16 claims paid shows NA/0 - verify if data gap or genuine",
        },
        "ai_readiness": [
            "Claim Settlement Ratio Analysis",
            "Insurance Penetration Trend Forecasting",
            "Scheme Effectiveness Classification (NAIS vs WBCIS)",
            "Anomaly Detection (Zero-claim years)",
            "RAG Context for Farmer Advisory on Insurance Eligibility",
        ],
        "recommended_complement": "PMFBY district-level data (2016+) via AIC/MoA portal",
        "krishisetu_mapping": {
            "use_case": "Crop insurance eligibility + claim settlement transparency",
            "rag_queries": [
                "What was the claim settlement ratio for Kharif 2014 in Maharashtra?",
                "How many farmers benefited from WBCIS vs NAIS?",
                "Is there a trend in insurance coverage growth?",
            ],
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
        "ds_crop_insurance_stats_mh",
        "Crop Insurance Statistics MH (2013-16)",
        "Agriculture",
        "https://data.gov.in/apis",
        metadata,
    ),
)

conn.commit()
cur.close()
conn.close()
print("✅ Cataloged Crop Insurance Statistics MH as HIGH PRIORITY for KrishiSetu")
