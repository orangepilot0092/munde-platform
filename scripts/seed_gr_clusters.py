import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from psycopg2.extras import Json
from src.core.config import settings
from src.core.embeddings import EmbeddingService


def seed_gr_clusters():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()
    es = EmbeddingService()

    # Ensure metadata column exists for tagging goals and horizons
    cur.execute(
        "ALTER TABLE document_registry ADD COLUMN IF NOT EXISTS metadata JSONB;"
    )
    conn.commit()

    grs = [
        {
            "id": 9996,
            "title": "GR: Jalyukt Shivar Abhiyan 2.0 (Drought Mitigation)",
            "domain": "Water Resources",
            "horizon": "long_term",
            "text": """GOVERNMENT OF MAHARASHTRA | WATER CONSERVATION DEPARTMENT
            Subject: Jalyukt Shivar Abhiyan 2.0 for Drought Mitigation.
            Long-Term Goal: Make 5,000 drought-prone villages tank-free over the next 5 years.
            Strategy: Decentralized water harvesting, desilting of rivers, and construction of check dams. 
            District Collectors must use MRSAC geospatial layers to identify catchment areas. 
            Budget allocation is tied to the KrishiSetu water stress index.""",
        },
        {
            "id": 9995,
            "title": "GR: Immediate Crop Insurance & DBT Integration",
            "domain": "Agriculture",
            "horizon": "short_term",
            "text": """GOVERNMENT OF MAHARASHTRA | AGRICULTURE DEPARTMENT
            Subject: Immediate Integration of PM-KISAN and PMFBY for upcoming Kharif season.
            Short-Term Goal: Ensure 100% direct benefit transfer (DBT) and crop insurance coverage for the current agricultural cycle.
            Action: APMC market data and Soil Health Card records must be synchronized immediately. 
            District Superintendents must use the Knowledge Graph to identify farmers in drought-prone talukas for priority insurance enrollment within 30 days.""",
        },
        {
            "id": 9994,
            "title": "GR: Dynamic Urban Water Rationing (NagarSetu)",
            "domain": "Urban Governance",
            "horizon": "short_term",
            "text": """GOVERNMENT OF MAHARASHTRA | URBAN DEVELOPMENT DEPARTMENT
            Subject: AI-Driven Water Rationing for Municipal Corporations.
            Short-Term Goal: Mitigate immediate water crisis due to delayed monsoons in PMC and MCGM.
            Action: Ingest daily reservoir levels from WRD and cross-reference with ward-wise population density. 
            Water pressure valves must be adjusted automatically based on predictive demand models starting this week. 
            Citizens will receive WhatsApp alerts via JanSetu regarding daily supply schedules.""",
        },
        {
            "id": 9993,
            "title": "GR: MPCB Industrial Green Transition Mandate",
            "domain": "Environment",
            "horizon": "long_term",
            "text": """GOVERNMENT OF MAHARASHTRA | ENVIRONMENT & CLIMATE CHANGE DEPARTMENT
            Subject: Mandatory Green Transition for MIDC Industrial Zones.
            Long-Term Goal: Achieve net-zero carbon emissions in all major MIDC estates by 2030.
            Strategy: Phased transition to renewable energy and zero-liquid discharge (ZLD) systems over the next 3 to 5 years. 
            MPCB will use satellite-based emission monitoring and IoT sensors to enforce compliance.""",
        },
        {
            "id": 9992,
            "title": "GR: Pre-Monsoon Flood Early Warning System",
            "domain": "Disaster Management",
            "horizon": "short_term",
            "text": """GOVERNMENT OF MAHARASHTRA | DISASTER MANAGEMENT & RELIEF
            Subject: Deployment of IoT Flood Sensors in Konkan and Western Maharashtra.
            Short-Term Goal: Establish real-time flood warning telemetry before the onset of the June monsoon.
            Action: SDMA to install automated weather stations and river gauge sensors in 50 high-risk talukas within 60 days. 
            Data must stream directly into the AapattiSetu dashboard for predictive evacuation modeling.""",
        },
        {
            "id": 9991,
            "title": "GR: MSRTC Electric Vehicle Fleet Expansion",
            "domain": "Transport",
            "horizon": "long_term",
            "text": """GOVERNMENT OF MAHARASHTRA | TRANSPORT DEPARTMENT
            Subject: MargSetu Initiative for Public Transport Electrification.
            Long-Term Goal: Transition 50% of the MSRTC bus fleet to electric vehicles (EV) by 2028.
            Strategy: Phased procurement of EV buses and construction of charging infrastructure at major depots over the next 4 years. 
            Route optimization algorithms will prioritize high-density corridors for initial EV deployment.""",
        },
        {
            "id": 9990,
            "title": "GR: Mahabhulekh 7/12 Complete Digitization Drive",
            "domain": "Land & GIS",
            "horizon": "short_term",
            "text": """GOVERNMENT OF MAHARASHTRA | REVENUE DEPARTMENT
            Subject: BhoomiSetu Mandate for Land Record Digitization.
            Short-Term Goal: Achieve 100% digitization and geo-tagging of all 7/12 extracts within 12 months.
            Action: Talathis must use the Sahyadri mobile app to verify plot boundaries against MRSAC satellite imagery. 
            Discrepancies must be flagged for immediate resolution by the Tehsildar.""",
        },
        {
            "id": 9989,
            "title": "GR: Statewide AI Skill Development Mission",
            "domain": "Education & Economy",
            "horizon": "long_term",
            "text": """GOVERNMENT OF MAHARASHTRA | SKILL DEVELOPMENT & ENTREPRENEURSHIP
            Subject: Preparing the workforce for the AI economy.
            Long-Term Goal: Train 1 million youth in AI, Data Science, and Green Tech over the next 5 years.
            Strategy: Partner with IT parks in Pune and Navi Mumbai to establish Centers of Excellence. 
            Curriculum will integrate with the Sahyadri Platform developer SDK for hands-on civic tech projects.""",
        },
    ]

    print("📄 Ingesting and Clustering Maharashtra Government Resolutions (GRs)...")
    for gr in grs:
        # 1. Insert parent document with metadata tags
        meta = Json(
            {
                "domain": gr["domain"],
                "time_horizon": gr["horizon"],
                "goal_type": "policy_resolution",
            }
        )

        cur.execute(
            """
            INSERT INTO document_registry (id, title, source_url, format, minio_path, file_hash, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET metadata = EXCLUDED.metadata
        """,
            (
                gr["id"],
                gr["title"],
                "https://gr.maharashtra.gov.in",
                "PDF",
                f"s3://documents/grs/{gr['id']}.pdf",
                f"hash_{gr['id']}",
                meta,
            ),
        )

        # 2. Generate embedding and insert chunk
        vec = es.generate_embedding(gr["text"])
        vec_str = "[" + ",".join(str(x) for x in vec) + "]"

        cur.execute(
            """
            INSERT INTO document_chunks (document_id, chunk_index, content, search_vector, embedding)
            VALUES (%s, 0, %s, to_tsvector('simple', %s), %s::vector)
            ON CONFLICT DO NOTHING
        """,
            (gr["id"], gr["text"], gr["text"], vec_str),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("🎉 SUCCESS! 8 GRs ingested and clustered by Short-Term and Long-Term goals.")


if __name__ == "__main__":
    seed_gr_clusters()
