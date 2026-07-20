import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)

sql = """
-- 1. Ensure GiST index exists for lightning-fast spatial queries
CREATE INDEX IF NOT EXISTS idx_admin_units_geom_gist 
ON administrative_units USING GIST (geometry);

-- 2. Add centroid and area columns if they don't exist
ALTER TABLE administrative_units ADD COLUMN IF NOT EXISTS centroid GEOMETRY(Point, 4326);
ALTER TABLE administrative_units ADD COLUMN IF NOT EXISTS area_sq_km DOUBLE PRECISION;

-- 3. Calculate and populate centroids and areas 
-- (ST_Area on geography cast calculates true surface area in sq meters on the WGS84 ellipsoid)
UPDATE administrative_units
SET 
    centroid = ST_Centroid(geometry),
    area_sq_km = ST_Area(geometry::geography) / 1000000.0
WHERE geometry IS NOT NULL AND (centroid IS NULL OR area_sq_km IS NULL);
"""

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()
print("✅ PostGIS GiST indexes added and centroids/areas calculated!")
