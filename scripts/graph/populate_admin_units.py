#!/usr/bin/env python3
"""Script to populate initial administrative units for Maharashtra."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.core.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.logging import get_logger

logger = get_logger(__name__)

MAHARASHTRA_DISTRICTS = [
    "Mumbai",
    "Pune",
    "Nagpur",
    "Thane",
    "Nashik",
    "Aurangabad",
    "Solapur",
    "Kolhapur",
    "Amravati",
    "Nanded",
    "Latur",
    "Dhule",
    "Jalgaon",
    "Akola",
    "Chandrapur",
    "Parbhani",
    "Beed",
    "Osmanabad",
    "Buldhana",
    "Wardha",
    "Washim",
    "Gondia",
    "Bhandara",
    "Gadchiroli",
    "Yavatmal",
    "Raigad",
    "Ratnagiri",
    "Sindhudurg",
    "Satara",
    "Sangli",
    "Ahmednagar",
    "Usmanabad",
    "Jalna",
    "Hingoli",
    "Palghar",
]


def main():
    logger.info("Starting Administrative Unit Population...")

    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # 1. Populate State and Districts
        state_query = text(
            "SELECT id FROM administrative_units WHERE name = 'Maharashtra' AND type = 'State'"
        )
        result = db.execute(state_query).fetchone()

        state_id = None
        if not result:
            insert_state = text("""
                INSERT INTO administrative_units (name, type, code) 
                VALUES ('Maharashtra', 'State', 'MH') RETURNING id
            """)
            state_id = db.execute(insert_state).scalar()
            logger.info(f"Created State: Maharashtra (ID: {state_id})")
        else:
            state_id = result[0]
            logger.info(f"Found State: Maharashtra (ID: {state_id})")

        for district_name in MAHARASHTRA_DISTRICTS:
            check_query = text(
                "SELECT id FROM administrative_units WHERE name = :name AND type = 'District'"
            )
            if not db.execute(check_query, {"name": district_name}).fetchone():
                insert_district = text("""
                    INSERT INTO administrative_units (name, type, parent_id) 
                    VALUES (:name, 'District', :parent_id)
                """)
                db.execute(
                    insert_district, {"name": district_name, "parent_id": state_id}
                )
                logger.info(f"Added District: {district_name}")

        db.commit()
        logger.info("✅ Administrative unit population complete.")

        # 2. Load Geometry if file exists
        geojson_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "gis",
            "maharashtra_districts_sample.geojson",
        )
        if os.path.exists(geojson_path):
            logger.info(f"Found GeoJSON at {geojson_path}. Loading geometry...")
            from src.knowledge_graph.gis_loader import GISLoader

            gis_loader = GISLoader(db)
            gis_loader.load_geojson(geojson_path)
        else:
            logger.warning(
                f"GeoJSON file not found at {geojson_path}. Skipping geometry load."
            )

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to populate units: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
