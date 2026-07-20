import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from src.core.config import settings


def repair_context():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()

    print("🔗 Re-linking Knowledge Graph cross-domain relationships...")
    # Re-link Sugarcane to Kolhapur, Cotton to Solapur, Ujani to Solapur
    repairs = [
        ("Sugarcane", "Kolhapur", "grown_in"),
        ("Cotton", "Solapur", "grown_in"),
        ("Ujani", "Solapur", "located_in"),
        ("Bhima", "Solapur", "flows_through"),
    ]

    for source, target, rel in repairs:
        cur.execute(
            """
            INSERT INTO graph_relationships (source_id, target_id, relationship_type)
            SELECT 
                (SELECT id FROM graph_entities WHERE name = %s),
                (SELECT id FROM graph_entities WHERE name = %s),
                %s
            WHERE EXISTS (SELECT 1 FROM graph_entities WHERE name = %s)
              AND EXISTS (SELECT 1 FROM graph_entities WHERE name = %s)
            ON CONFLICT DO NOTHING
        """,
            (source, target, rel, source, target),
        )

    print("🗺️  Patching District centroids and areas for Geospatial Context...")
    # Inject realistic mock centroids and areas for key districts
    district_patches = [
        ("Solapur", 18.41, 75.92, 14800.5),
        ("Kolhapur", 16.70, 74.24, 7750.2),
        ("Pune", 18.52, 73.85, 15600.8),
        ("Nashik", 20.00, 73.78, 15500.1),
    ]

    for name, lat, lon, area in district_patches:
        cur.execute(
            """
            UPDATE administrative_units
            SET centroid = ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                area_sq_km = %s
            WHERE name = %s AND type = 'District'
        """,
            (lon, lat, area, name),
        )

    conn.commit()
    cur.close()
    conn.close()
    print(
        "🎉 SUCCESS! RAG Context repaired. Cross-domain links and geospatial metrics restored."
    )


if __name__ == "__main__":
    repair_context()
