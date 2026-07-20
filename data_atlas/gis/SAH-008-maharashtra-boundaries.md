# SAH-008: Maharashtra Administrative Boundaries

## Basic Information
- **Dataset ID:** SAH-008
- **Dataset Name:** Maharashtra District and Taluka Boundaries
- **Description:** Official administrative boundaries for Maharashtra's 36 Districts and ~358 Talukas. This layer is essential for aggregating and visualizing all domain-specific data.
- **Domain:** Governance / GIS
- **Category:** Vector Polygon Data
- **Tags:** boundaries, districts, talukas, gis, administration

## Ownership
- **Department:** Survey of India / Maharashtra State Department of Town Planning & Valuation
- **Data Owner:** Government of Maharashtra
- **Publishing Organization:** Bhuvan (ISRO) / OGD India
- **Official Website:** https://bhuvan.nrsc.gov.in/

## Source Information
- **Official URL:** https://data.gov.in/
- **Download URL:** Available via OGD India portal or Bhuvan.
- **Documentation:** https://bhuvan.nrsc.gov.in/bhugyantham/
- **Authentication Method:** None for public downloads.
- **Access Restrictions:** None.

## Legal Information
- **License:** Open Government Data (OGD) License
- **Terms of Use:** Attribution required.

## Update Information
- **Refresh Frequency:** Annual (or as per administrative reorganization)
- **Historical Coverage:** Current administrative structure.

## Technical Information
- **Format:** Shapefile, GeoJSON
- **Spatial Reference System:** EPSG:4326 (WGS 84)
- **Geographic Coverage:** 
  - State: Maharashtra
  - Districts: 36
  - Talukas: ~358

## ETL Specification
- **Source Connector:** File Download (Shapefile/GeoJSON)
- **Download Strategy:** One-time bulk load, then check for annual updates.
- **Validation Rules:** Ensure no overlapping polygons and valid topology.
- **Storage Destination:** PostgreSQL + PostGIS (gis schema)

## Knowledge Graph Mapping
- **Entities:** District, Taluka, Village.
- **Relationships:** contains, belongs_to, adjacent_to.

## AI Readiness Assessment
- **Geospatial Analytics:** Essential for choropleth maps and regional aggregation.
- **RAG:** Allows users to ask questions like "Show me water levels in Nashik district."
