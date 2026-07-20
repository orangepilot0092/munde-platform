# SAH-006: NASA FIRMS Fire Hotspots

## Basic Information
- **Dataset ID:** SAH-006
- **Dataset Name:** NASA FIRMS Active Fire Data
- **Description:** Near real-time active fire locations detected by MODIS and VIIRS satellites. Critical for monitoring forest fires in Western Ghats and agricultural residue burning.
- **Domain:** Disaster Management / Environment
- **Category:** Satellite Derived / Point Data
- **Tags:** fire, hotspot, nasa, firms, disaster, modis, viirs

## Ownership
- **Department:** NASA
- **Data Owner:** Earth Science Data and Information System (ESDIS)
- **Publishing Organization:** NASA FIRMS
- **Official Website:** https://firms.modaps.eosdis.nasa.gov/

## Source Information
- **Official URL:** https://firms.modaps.eosdis.nasa.gov/
- **API Endpoint:** https://firms.modaps.eosdis.nasa.gov/api/
- **Documentation:** https://firms.modaps.eosdis.nasa.gov/api/
- **Authentication Method:** None (Public)
- **Access Restrictions:** None.

## Legal Information
- **License:** Public Domain
- **Terms of Use:** No restrictions.

## Update Information
- **Refresh Frequency:** Daily (MODIS) / Near Real-time (VIIRS)
- **Historical Coverage:** Since 2000 (MODIS)

## Technical Information
- **Format:** CSV, GeoJSON, KML
- **Spatial Reference System:** EPSG:4326 (WGS 84)
- **Geographic Coverage:** Global (including all of Maharashtra)

## ETL Specification
- **Source Connector:** REST API / Direct Download
- **Download Strategy:** Daily download of Maharashtra bounding box.
- **Validation Rules:** Filter out low-confidence detections if necessary.
- **Storage Destination:** PostgreSQL + PostGIS (disaster schema)

## Knowledge Graph Mapping
- **Entities:** Fire Hotspot, Forest Area, Agricultural Land.
- **Relationships:** located_in, affects, detected_by.

## AI Readiness Assessment
- **Computer Vision:** Correlate hotspots with Sentinel-2 imagery for burn scar analysis.
- **Forecasting:** Predict fire risk based on weather (IMD) and vegetation dryness.
