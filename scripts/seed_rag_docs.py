import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from src.core.config import settings
from src.core.embeddings import EmbeddingService


def seed_rag_docs():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()
    es = EmbeddingService()

    # Ensure 'format' column exists in document_registry
    cur.execute(
        "ALTER TABLE document_registry ADD COLUMN IF NOT EXISTS format VARCHAR(50);"
    )
    conn.commit()

    docs = [
        {
            "id": 9998,
            "title": "Maharashtra GR: PM-KISAN & Crop Insurance Integration",
            "domain": "Agriculture",
            "text": """
            GOVERNMENT OF MAHARASHTRA
            AGRICULTURE DEPARTMENT
            Government Resolution No. AGRI-2024/CR-456/Farmers
            Subject: Integration of PM-KISAN and PMFBY with KrishiSetu.
            
            To ensure direct benefit transfer (DBT) and crop insurance coverage, the Agriculture Department mandates 
            that all APMC market data and Soil Health Card records be synchronized with the Sahyadri Platform. 
            District Superintendents of Agriculture must use the Knowledge Graph to identify farmers in drought-prone 
            talukas for priority insurance enrollment. AI models must be trained on historical APMC arrival prices 
            to forecast market gluts.
            """,
        },
        {
            "id": 9997,
            "title": "Maharashtra GR: NagarSetu Urban Water Rationing",
            "domain": "Urban Governance",
            "text": """
            GOVERNMENT OF MAHARASHTRA
            URBAN DEVELOPMENT DEPARTMENT
            Government Resolution No. UD-2024/CR-789/NagarSetu
            Subject: AI-Driven Water Rationing for Municipal Corporations.
            
            Due to delayed monsoons, Pune (PMC) and Mumbai (MCGM) must implement dynamic water rationing. 
            The NagarSetu platform will ingest daily reservoir levels from WRD and cross-reference them with 
            ward-wise population density from the Census 2011 dataset. Water pressure valves must be adjusted 
            automatically based on the predictive demand model. Citizens will receive WhatsApp alerts via JanSetu 
            regarding their ward's water supply schedule.
            """,
        },
    ]

    print("📄 Ingesting Agriculture and Urban Governance GRs into Vector DB...")
    for doc in docs:
        # 1. Insert parent document (including dummy minio_path and file_hash to satisfy NOT NULL constraints)
        cur.execute(
            """
            INSERT INTO document_registry (id, title, source_url, format, minio_path, file_hash)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """,
            (
                doc["id"],
                doc["title"],
                "https://gr.maharashtra.gov.in",
                "PDF",
                f"s3://documents/grs/{doc['id']}.pdf",
                f"dummy_hash_{doc['id']}",
            ),
        )

        # 2. Generate embedding and insert chunk
        vec = es.generate_embedding(doc["text"])
        vec_str = "[" + ",".join(str(x) for x in vec) + "]"

        cur.execute(
            """
            INSERT INTO document_chunks (document_id, chunk_index, content, search_vector, embedding)
            VALUES (%s, 0, %s, to_tsvector('simple', %s), %s::vector)
            ON CONFLICT DO NOTHING
        """,
            (doc["id"], doc["text"], doc["text"], vec_str),
        )

    conn.commit()
    cur.close()
    conn.close()
    print(
        "🎉 SUCCESS! Vector DB now holds Water, Agriculture, and Urban policies for RAG testing."
    )


if __name__ == "__main__":
    seed_rag_docs()
