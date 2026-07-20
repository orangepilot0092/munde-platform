import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class GISLoader:
    def __init__(self, db_session: Session):
        self.db = db_session

    def load_geojson(self, file_path: str):
        """Load GeoJSON features into the administrative_units table."""
        logger.info(f"Loading GeoJSON from {file_path}")

        with open(file_path, "r") as f:
            data = json.load(f)

        count = 0
        for feature in data["features"]:
            name = feature["properties"].get("name")
            if not name:
                continue

            # Find the existing unit
            query = text(
                "SELECT id FROM administrative_units WHERE name = :name AND type = 'District'"
            )
            result = self.db.execute(query, {"name": name}).fetchone()

            if result:
                unit_id = result[0]
                geom = shape(feature["geometry"])
                wkb_element = from_shape(geom, srid=4326)

                update_query = text("""
                    UPDATE administrative_units 
                    SET geometry = ST_GeomFromWKB(:geom, 4326) 
                    WHERE id = :id
                """)
                self.db.execute(update_query, {"geom": wkb_element.data, "id": unit_id})
                count += 1

        self.db.commit()
        logger.info(f"✅ Updated geometry for {count} districts.")
