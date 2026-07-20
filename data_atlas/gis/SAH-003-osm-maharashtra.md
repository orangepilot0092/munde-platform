# SAH-003: OpenStreetMap (OSM) - Maharashtra

## Basic Information
- **Dataset ID:** SAH-003
- **Dataset Name:** OpenStreetMap Geospatial Data
- **Description:** Collaborative, free, and editable map of the world. For Sahyadri, this provides the base layer for roads, buildings, railways, waterways, and points of interest (POIs) in Maharashtra.
- **Domain:** Geospatial / GIS
- **Category:** Vector Map Data
- **Tags:** osm, gis, maps, roads, buildings, poi

## Ownership
- **Department:** OpenStreetMap Foundation
- **Data Owner:** Community Contributors
- **Publishing Organization:** OpenStreetMap Foundation
- **Official Website:** https://www.openstreetmap.org/

## Source Information
- **Official URL:** https://www.openstreetmap.org/
- **API Endpoint:** https://overpass-api.de/ (Overpass Turbo)
- **Documentation:** https://wiki.openstreetmap.org/wiki/API
- **Authentication Method:** None for read-only; OAuth for editing.
- **Access Restrictions:** None (Open Data Commons Open Database License).

## Legal Information
- **License:** Open Data Commons Open Database License (ODbL)
- **Terms of Use:** Attribution required ("© OpenStreetMap contributors").

## Update Information
- **Refresh Frequency:** Real-time (community-driven)
- **Historical Coverage:** Full history available via planet files.

## Technical Information
- **Format:** XML, PBF, GeoJSON
- **Spatial Reference System:** EPSG:4326 (WGS 84)
- **Geographic Coverage:** 
  - State: Maharashtra
  - District: All
  - Taluka: All
  - Village: Major villages covered

## ETL Specification
- **Source Connector:** Overpass API / Geofabrik Downloads
- **Download Strategy:** Daily extracts for Maharashtra from Geofabrik or live queries via Overpass for specific features.
- **Validation Rules:** Topology checks (no overlapping polygons, valid coordinates).
- **Storage Destination:** PostgreSQL + PostGIS (gis schema)

## Knowledge Graph Mapping
- **Entities:** Road, Building, Hospital, School, Market, River.
- **Relationships:** connects_to, located_in, serves.

## AI Readiness Assessment
- **Geospatial Analytics:** Essential for routing, proximity analysis, and urban planning models.
- **Computer Vision:** Can be used as ground truth for satellite imagery segmentation.
