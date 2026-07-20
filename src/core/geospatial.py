from sqlalchemy.orm import Session
from sqlalchemy import text


class GeospatialService:
    def __init__(self, db: Session):
        self.db = db

    def get_district_metrics(self, name: str):
        sql = text("""
            SELECT name, area_sq_km, 
                   ST_X(centroid) as longitude, 
                   ST_Y(centroid) as latitude
            FROM administrative_units 
            WHERE name = :name AND type = 'District'
        """)
        res = self.db.execute(sql, {"name": name}).first()
        if not res:
            return None
        return {
            "name": res.name,
            "area_sq_km": round(res.area_sq_km, 2) if res.area_sq_km else None,
            "centroid": {"lat": res.latitude, "lon": res.longitude}
            if res.latitude
            else None,
        }

    def get_all_centroids(self):
        sql = text("""
            SELECT name, ST_X(centroid) as longitude, ST_Y(centroid) as latitude, area_sq_km
            FROM administrative_units
            WHERE type = 'District' AND centroid IS NOT NULL
        """)
        res = self.db.execute(sql).fetchall()
        return [
            {
                "name": r.name,
                "lat": r.latitude,
                "lon": r.longitude,
                "area_sq_km": round(r.area_sq_km, 2),
            }
            for r in res
        ]

    def find_intersecting_features(self, target_name: str):
        # Finds what other districts/features share a border or overlap with the target
        sql = text("""
            SELECT a.name as target, b.name as intersecting_feature, b.type as feature_type
            FROM administrative_units a
            JOIN administrative_units b ON ST_Intersects(a.geometry, b.geometry)
            WHERE a.name = :name AND a.id != b.id
        """)
        res = self.db.execute(sql, {"name": target_name}).fetchall()
        return [
            {
                "target": r.target,
                "intersecting_feature": r.intersecting_feature,
                "type": r.feature_type,
            }
            for r in res
        ]
