import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from psycopg2.extras import Json
from src.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()

datasets = [
    {
        "dataset_id": "ds_land_use_pattern_mh",
        "name": "Land Use Pattern - Maharashtra (Baseline)",
        "domain": "Land Intelligence",
        "source_url": "https://data.gov.in/catalog/land-use-pattern-maharashtra",
        "metadata": {
            "resource_id": "TO_BE_EXTRACTED",
            "dataset_name": "Land Use Pattern - Maharashtra",
            "department": "NITI Aayog",
            "source": "Data.gov.in",
            "license": "GODL",
            "refresh_frequency": "Annual",
            "last_updated": "2025-06-02",
            "geographic_resolution": "State-level aggregate",
            "priority": "high",
            "schema_fields": ["Land_Use_Category", "Area_Thousands_Ha", "Percentage"],
            "data_snapshot": {"net_area_sown_pct": 56.66, "forest_cover_pct": 16.95},
            "ai_readiness": [
                "Land Use Classification",
                "Crop Planning Context",
                "Water Stress Modeling",
            ],
            "verified_date": "2026-07-09",
        },
    },
    {
        "dataset_id": "ds_crop_insurance_stats_mh",
        "name": "Crop Insurance Statistics MH (2013-16)",
        "domain": "Agriculture",
        "source_url": "https://data.gov.in/apis",
        "metadata": {
            "resource_id": "TO_BE_EXTRACTED",
            "dataset_name": "Business Statistics of Crop Insurance Schemes in Maharashtra (2013-16)",
            "department": "Ministry of Agriculture and Farmers Welfare",
            "source": "Data.gov.in",
            "license": "GODL",
            "refresh_frequency": "Historical compilation",
            "last_updated": "2026-02-25",
            "temporal_coverage": "2013-14 to 2015-16",
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
                "schemes": ["NAIS", "WBCIS"],
            },
            "ai_readiness": [
                "Claim Settlement Ratio Analysis",
                "Insurance Penetration Forecasting",
                "Scheme Effectiveness Classification",
            ],
            "verified_date": "2026-07-09",
        },
    },
    {
        "dataset_id": "ds_forest_cover_district_mh_2011",
        "name": "District-wise Forest Cover MH 2011 (Baseline)",
        "domain": "Environment",
        "source_url": "https://api.data.gov.in/resource/84d26d02-935b-479c-9427-c27ee1afd76f",
        "metadata": {
            "resource_id": "84d26d02-935b-479c-9427-c27ee1afd76f",
            "dataset_name": "District-wise Forest Cover - Maharashtra (2011 Assessment)",
            "department": "NITI Aayog / FSI",
            "source": "Data.gov.in",
            "license": "GODL",
            "geographic_resolution": "District-level (35 districts)",
            "priority": "medium-high",
            "schema_fields": [
                "District",
                "Geographical_Area_SqKm",
                "VDF_SqKm",
                "MDF_SqKm",
                "Open_Forest_SqKm",
                "Total_Forest_SqKm",
                "Percent_of_GA",
                "Change_SqKm",
                "Scrub_SqKm",
            ],
            "data_snapshot": {
                "state_total_forest_pct": 16.46,
                "highest_cover": "Gadchiroli (70.04%)",
                "lowest_cover": "Latur (0.07%)",
            },
            "ai_readiness": [
                "Historical Baseline for Change Detection",
                "Deforestation Hotspot Classification",
                "Afforestation Target Identification",
            ],
            "verified_date": "2026-07-09",
        },
    },
    {
        "dataset_id": "ds_energy_balance_monthly_mh",
        "name": "MH Monthly Energy Balance (2021-25)",
        "domain": "Energy",
        "source_url": "https://data.gov.in/apis",
        "metadata": {
            "resource_id": "TO_BE_EXTRACTED",
            "dataset_name": "Maharashtra Monthly Energy Supply-Demand Balance (Apr 2021 - Feb 2025)",
            "department": "Ministry of Power / CEA",
            "source": "Data.gov.in",
            "license": "GODL",
            "refresh_frequency": "Monthly",
            "last_updated": "2025-02-28",
            "temporal_coverage": "2021-04 to 2025-02 (47 months)",
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
                "worst_peak_deficit": "Sep-24 (11.7%, 3506 MW)",
                "zero_deficit_months": 35,
                "demand_growth_cagr_pct": 4.3,
            },
            "ai_readiness": [
                "Monthly Load Forecasting",
                "Peak Deficit Early Warning",
                "Seasonal Pattern Classification",
                "Anomaly Detection",
            ],
            "verified_date": "2026-07-09",
        },
    },
    {
        "dataset_id": "ds_pmkusum_solar_pumps_mh",
        "name": "PM-KUSUM Solar Pump Installation MH (District-wise)",
        "domain": "Energy",
        "source_url": "https://data.gov.in/apis",
        "metadata": {
            "resource_id": "TO_BE_EXTRACTED",
            "dataset_name": "PM-KUSUM Solar Pump Installation - District-wise Maharashtra",
            "department": "Ministry of New & Renewable Energy / MEDA",
            "source": "Data.gov.in",
            "license": "GODL",
            "geographic_resolution": "District-level (36 districts)",
            "priority": "high",
            "schema_fields": [
                "District",
                "Component_A_MW_Installed",
                "Component_B_Pumps_Installed",
                "Component_C_FLS_Pumps_Solarized",
            ],
            "data_snapshot": {
                "total_pumps": 290559,
                "total_feeder_solarizations": 74674,
                "zero_adoption_districts": 5,
            },
            "ai_readiness": [
                "District Adoption Gap Analysis",
                "Solar Irrigation Penetration Forecasting",
                "Cross-domain RAG Context",
            ],
            "cross_domain": ["UrjaSetu", "KrishiSetu"],
            "verified_date": "2026-07-09",
        },
    },
    {
        "dataset_id": "ds_udyam_msme_mh",
        "name": "UDYAM MSME Registration (Maharashtra)",
        "domain": "Industry",
        "source_url": "https://api.data.gov.in/resource/8b68ae56-84cf-4728-a0a6-1be11028dea7",
        "metadata": {
            "resource_id": "8b68ae56-84cf-4728-a0a6-1be11028dea7",
            "dataset_name": "List of MSME Registered Units under UDYAM",
            "department": "Ministry of MSME",
            "source": "Data.gov.in",
            "license": "GODL",
            "refresh_frequency": "Daily",
            "last_updated": "2026-07-08",
            "total_records_national": 41546353,
            "maharashtra_filter": {"field": "LG_ST_Code", "value": "27"},
            "priority": "medium",
            "schema_fields": [
                "Activities",
                "CommunicationAddress",
                "District",
                "EnterpriseName",
                "LG_DT_Code",
                "LG_ST_Code",
                "Pincode",
                "RegistrationDate",
                "State",
            ],
            "key_finding": "Use LG_ST_Code=27 for Maharashtra. State names are UPPERCASE.",
            "ai_readiness": ["Clustering", "Classification", "Geospatial Analytics"],
            "verified_date": "2026-07-09",
        },
    },
]

for ds in datasets:
    cur.execute(
        """
        INSERT INTO metadata_registry (dataset_id, name, domain, source_url, metadata)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (dataset_id) DO UPDATE SET 
            name = EXCLUDED.name,
            domain = EXCLUDED.domain,
            source_url = EXCLUDED.source_url,
            metadata = EXCLUDED.metadata
    """,
        (
            ds["dataset_id"],
            ds["name"],
            ds["domain"],
            ds["source_url"],
            Json(ds["metadata"]),
        ),
    )
    print(f"✅ {ds['dataset_id']}")

conn.commit()
cur.close()
conn.close()
print(f"\n🎉 All {len(datasets)} datasets cataloged successfully!")
