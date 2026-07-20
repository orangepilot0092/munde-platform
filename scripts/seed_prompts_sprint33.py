"""
Sprint 33 — Seed Prompt Registry
Uses os.environ directly to avoid settings module caching localhost DB URL.
"""

import os
import psycopg2
from psycopg2.extras import Json

# Read DATABASE_URL directly from environment (bypasses cached settings)
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

prompts = [
    {
        "prompt_id": "bhoomisetu_hospital_finder",
        "name": "BhoomiSetu Hospital Finder RAG",
        "domain": "bhoomisetu",
        "category": "rag_qa",
        "system_prompt": "You are BhoomiSetu, Maharashtra's land and infrastructure intelligence assistant. Answer questions about healthcare facilities using verified OpenStreetMap data. Always cite the hospital name and location. If no data is available, say so clearly.",
        "user_template": "Find hospitals near {district} district. How many are there and what are their names?",
        "variables": {"district": "string"},
        "tags": ["geospatial", "healthcare", "osm", "rag"],
        "metadata": {
            "data_source": "osm_overpass",
            "query_type": "hospitals",
            "verified_element_count": 7620,
        },
    },
    {
        "prompt_id": "jalsetu_weather_advisory",
        "name": "JalSetu Weather-Based Water Advisory",
        "domain": "jalsetu",
        "category": "forecasting",
        "system_prompt": "You are JalSetu, Maharashtra's water intelligence assistant. Use Open-Meteo forecast data to provide actionable water management advisories. Include precipitation forecasts, temperature trends, and specific recommendations for irrigation or water conservation.",
        "user_template": "What is the 7-day weather forecast for {location}? Should farmers irrigate this week?",
        "variables": {"location": "string"},
        "tags": ["weather", "water", "agriculture", "open-meteo"],
        "metadata": {
            "data_source": "open_meteo_pune",
            "forecast_days": 7,
            "timezone": "Asia/Kolkata",
        },
    },
    {
        "prompt_id": "krishisetu_crop_insurance_qa",
        "name": "KrishiSetu Crop Insurance Q&A",
        "domain": "krishisetu",
        "category": "rag_qa",
        "system_prompt": "You are KrishiSetu, Maharashtra's agriculture intelligence assistant. Answer crop insurance questions using verified government statistics. Cite scheme names (NAIS/WBCIS/PMFBY), coverage figures, and claim settlement ratios. Distinguish between historical data and current schemes.",
        "user_template": "What was the claim settlement ratio for {scheme} in Maharashtra during {year}?",
        "variables": {"scheme": "string", "year": "string"},
        "tags": ["agriculture", "insurance", "policy", "rag"],
        "metadata": {
            "data_source": "ds_crop_insurance_stats_mh",
            "temporal_coverage": "2013-2016",
        },
    },
    {
        "prompt_id": "urjasetu_energy_deficit_alert",
        "name": "UrjaSetu Energy Deficit Early Warning",
        "domain": "urjasetu",
        "category": "classification",
        "system_prompt": "You are UrjaSetu, Maharashtra's energy intelligence assistant. Analyze monthly energy supply-demand data to classify deficit severity and recommend actions. Use thresholds: >5% peak deficit = WARNING, >10% = CRITICAL. Cite specific months and MW values.",
        "user_template": "Analyze Maharashtra's energy deficit pattern for {season}. What alerts should be issued?",
        "variables": {"season": "string"},
        "tags": ["energy", "deficit", "alerting", "time-series"],
        "metadata": {
            "data_source": "ds_energy_balance_monthly_mh",
            "alert_thresholds": {"warning": 5, "critical": 10},
        },
    },
    {
        "prompt_id": "paryavaran_forest_cover_change",
        "name": "Paryavaran Forest Cover Change Analysis",
        "domain": "paryavaran",
        "category": "summarization",
        "system_prompt": "You are Paryavaran, Maharashtra's environmental intelligence assistant. Summarize forest cover changes by district using verified FSI/NITI Aayog data. Highlight districts with significant loss or gain, scrub land conversion potential, and compare against state average (16.46%).",
        "user_template": "Summarize forest cover status for {district}. Is it above or below state average? Any notable changes?",
        "variables": {"district": "string"},
        "tags": ["environment", "forest", "change-detection", "baseline"],
        "metadata": {
            "data_source": "ds_forest_cover_district_mh_2011",
            "state_avg_pct": 16.46,
        },
    },
]

for p in prompts:
    cur.execute(
        """
        INSERT INTO prompt_registry 
            (prompt_id, name, domain, category, system_prompt, user_template, variables, tags, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (prompt_id, version) DO UPDATE SET
            name = EXCLUDED.name,
            system_prompt = EXCLUDED.system_prompt,
            user_template = EXCLUDED.user_template,
            variables = EXCLUDED.variables,
            tags = EXCLUDED.tags,
            metadata = EXCLUDED.metadata,
            updated_at = NOW()
    """,
        (
            p["prompt_id"],
            p["name"],
            p["domain"],
            p["category"],
            p["system_prompt"],
            p.get("user_template"),
            Json(p.get("variables")),
            p.get("tags"),
            Json(p.get("metadata")),
        ),
    )
    print(f"✅ Seeded: {p['prompt_id']} ({p['domain']}/{p['category']})")

conn.commit()
cur.close()
conn.close()
print(f"\n🎉 All {len(prompts)} prompts seeded successfully!")
