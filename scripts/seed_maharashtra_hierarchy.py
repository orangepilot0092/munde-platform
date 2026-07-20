import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from psycopg2.extras import execute_values
from src.core.config import settings
import random

# 1. Real 36 Districts with approximate bounding boxes (min_lat, max_lat, min_lon, max_lon)
districts_meta = {
    "Mumbai": (18.89, 19.28, 72.77, 72.99),
    "Mumbai Suburban": (19.08, 19.27, 72.80, 72.98),
    "Thane": (19.15, 19.60, 72.85, 73.35),
    "Palghar": (19.50, 20.10, 72.60, 73.10),
    "Raigad": (17.80, 18.70, 73.10, 73.90),
    "Ratnagiri": (16.50, 17.50, 73.10, 73.90),
    "Sindhudurg": (15.60, 16.50, 73.50, 74.20),
    "Nashik": (19.50, 20.50, 73.20, 74.50),
    "Jalgaon": (20.50, 21.50, 74.50, 76.20),
    "Dhule": (20.50, 21.50, 73.80, 75.20),
    "Nandurbar": (20.80, 21.80, 73.50, 74.80),
    "Pune": (17.80, 19.20, 73.20, 75.20),
    "Satara": (16.80, 18.20, 73.50, 74.80),
    "Sangli": (16.30, 17.50, 74.00, 75.20),
    "Kolhapur": (15.60, 17.10, 73.80, 75.10),
    "Solapur": (17.10, 18.60, 74.50, 76.50),
    "Ahmednagar": (18.20, 19.90, 73.50, 75.30),
    "Aurangabad": (19.20, 20.50, 74.50, 76.00),
    "Jalna": (19.20, 20.30, 75.20, 76.50),
    "Parbhani": (18.50, 20.10, 76.00, 77.50),
    "Hingoli": (19.20, 20.10, 76.50, 77.60),
    "Nanded": (18.20, 19.80, 77.00, 78.50),
    "Beed": (18.00, 19.50, 75.00, 76.50),
    "Latur": (17.50, 19.00, 76.00, 78.00),
    "Osmanabad": (17.50, 18.80, 75.50, 77.00),
    "Buldhana": (20.00, 21.30, 75.50, 77.00),
    "Akola": (20.20, 21.20, 76.50, 77.80),
    "Washim": (19.50, 20.50, 76.50, 77.80),
    "Amravati": (20.50, 21.80, 76.80, 78.20),
    "Yavatmal": (19.20, 20.80, 77.50, 79.00),
    "Wardha": (20.00, 21.20, 78.00, 79.20),
    "Nagpur": (20.50, 21.80, 78.50, 79.80),
    "Bhandara": (20.50, 21.50, 79.20, 80.20),
    "Gondia": (20.80, 21.80, 79.80, 80.80),
    "Chandrapur": (19.00, 20.50, 78.50, 80.00),
    "Gadchiroli": (19.00, 20.80, 79.50, 80.80),
}

# Realistic Taluka counts per district (Total ~353)
taluka_counts = {
    "Mumbai": 3,
    "Mumbai Suburban": 3,
    "Thane": 7,
    "Palghar": 8,
    "Raigad": 15,
    "Ratnagiri": 11,
    "Sindhudurg": 8,
    "Nashik": 15,
    "Jalgaon": 15,
    "Dhule": 4,
    "Nandurbar": 6,
    "Pune": 14,
    "Satara": 11,
    "Sangli": 10,
    "Kolhapur": 12,
    "Solapur": 11,
    "Ahmednagar": 14,
    "Aurangabad": 9,
    "Jalna": 8,
    "Parbhani": 9,
    "Hingoli": 5,
    "Nanded": 16,
    "Beed": 11,
    "Latur": 10,
    "Osmanabad": 8,
    "Buldhana": 13,
    "Akola": 7,
    "Washim": 6,
    "Amravati": 14,
    "Yavatmal": 16,
    "Wardha": 8,
    "Nagpur": 14,
    "Bhandara": 7,
    "Gondia": 8,
    "Chandrapur": 15,
    "Gadchiroli": 12,
}


def seed_hierarchy():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()

    # 1. Schema Upgrade
    cur.execute(
        "ALTER TABLE administrative_units ADD COLUMN IF NOT EXISTS parent_name VARCHAR(255);"
    )
    conn.commit()

    print("🧹 Clearing existing administrative hierarchy to prevent duplicates...")

    cur.execute(
        "SELECT id FROM graph_entities WHERE type IN ('State', 'District', 'Taluka', 'Village')"
    )
    admin_ids = [row[0] for row in cur.fetchall()]

    if admin_ids:
        cur.execute(
            "DELETE FROM graph_relationships WHERE source_id = ANY(%s) OR target_id = ANY(%s)",
            (admin_ids, admin_ids),
        )
        cur.execute(
            "DELETE FROM graph_entities WHERE type IN ('State', 'District', 'Taluka', 'Village')"
        )

    cur.execute(
        "DELETE FROM administrative_units WHERE type IN ('State', 'District', 'Taluka', 'Village')"
    )
    conn.commit()

    entities = [("Maharashtra", "State", None)]
    admin_units = []
    village_counter = 0

    print("🏗️  Generating 36 Districts, 353 Talukas, and ~43,000 Villages...")

    for district, bbox in districts_meta.items():
        min_lat, max_lat, min_lon, max_lon = bbox
        entities.append((district, "District", None))
        admin_units.append((district, "District", "Maharashtra", None, 0.0))

        t_count = taluka_counts[district]
        for t in range(1, t_count + 1):
            taluka_name = f"{district}_Taluka_{t}"
            entities.append((taluka_name, "Taluka", None))
            admin_units.append((taluka_name, "Taluka", district, None, 0.0))

            v_count = random.randint(115, 125)
            for v in range(1, v_count + 1):
                village_name = f"Village_{village_counter}"
                lat = random.uniform(min_lat, max_lat)
                lon = random.uniform(min_lon, max_lon)
                geom_wkt = f"SRID=4326;POINT({lon} {lat})"

                entities.append((village_name, "Village", None))
                admin_units.append(
                    (village_name, "Village", taluka_name, geom_wkt, 0.0)
                )
                village_counter += 1

    print(
        f"✅ Generated {len(entities)} entities and {len(admin_units)} spatial records."
    )
    print("💾 Bulk inserting into Knowledge Graph...")

    # Insert without RETURNING to avoid psycopg2 chunking issues
    execute_values(
        cur, "INSERT INTO graph_entities (name, type, metadata) VALUES %s", entities
    )

    # Fetch IDs via a single SELECT query instead of relying on chunked RETURNING
    print("🔍 Fetching generated entity IDs...")
    cur.execute(
        "SELECT id, name FROM graph_entities WHERE type IN ('State', 'District', 'Taluka', 'Village')"
    )
    entity_ids = {row[1]: row[0] for row in cur.fetchall()}

    print("💾 Bulk inserting into PostGIS administrative_units...")
    execute_values(
        cur,
        "INSERT INTO administrative_units (name, type, parent_name, centroid, area_sq_km) VALUES %s",
        admin_units,
        template="(%s, %s, %s, ST_GeomFromEWKT(%s), %s)",
    )

    print("🕸️  Building Graph Relationships (belongs_to)...")
    relationships = []
    state_id = entity_ids["Maharashtra"]
    for district in districts_meta.keys():
        relationships.append((entity_ids[district], state_id, "belongs_to"))
        t_count = taluka_counts[district]
        for t in range(1, t_count + 1):
            taluka_name = f"{district}_Taluka_{t}"
            relationships.append(
                (entity_ids[taluka_name], entity_ids[district], "belongs_to")
            )

    execute_values(
        cur,
        "INSERT INTO graph_relationships (source_id, target_id, relationship_type) VALUES %s ON CONFLICT DO NOTHING",
        relationships,
    )

    conn.commit()
    cur.close()
    conn.close()
    print(
        f"🎉 SUCCESS! Ingested 1 State, 36 Districts, 353 Talukas, and {village_counter} Villages!"
    )


if __name__ == "__main__":
    seed_hierarchy()
