# SAH-007: USGS Earthquake Data

## Basic Information
- **Dataset ID:** SAH-007
- **Dataset Name:** USGS Real-time Earthquake Data
- **Description:** Global earthquake data provided by the United States Geological Survey. Includes magnitude, depth, location, and time. Critical for monitoring seismic activity in Maharashtra's coastal and inland regions.
- **Domain:** Disaster Management / Geology
- **Category:** Real-time Event Data
- **Tags:** earthquake, usgs, seismic, disaster, real-time

## Ownership
- **Department:** United States Geological Survey (USGS)
- **Data Owner:** USGS Earthquake Hazards Program
- **Publishing Organization:** USGS
- **Official Website:** https://earthquake.usgs.gov/

## Source Information
- **Official URL:** https://earthquake.usgs.gov/earthquakes/map/
- **API Endpoint:** https://earthquake.usgs.gov/fdsnws/prod/
- **Documentation:** https://usgs.github.io/earthquake-api/
- **Authentication Method:** None (Public)
- **Access Restrictions:** None.

## Legal Information
- **License:** Public Domain
- **Terms of Use:** No restrictions.

## Update Information
- **Refresh Frequency:** Real-time (minutes)
- **Historical Coverage:** Since 1960s (varies by region)

## Technical Information
- **Format:** GeoJSON, CSV, KML
- **Spatial Reference System:** EPSG:4326 (WGS 84)
- **Geographic Coverage:** Global (including Maharashtra)

## ETL Specification
- **Source Connector:** REST API (GeoJSON feed)
- **Download Strategy:** Poll every 15 minutes for events within Maharashtra bounding box.
- **Validation Rules:** Filter out events with magnitude < 2.0 unless near critical infrastructure.
- **Storage Destination:** PostgreSQL + PostGIS (disaster schema)

## Knowledge Graph Mapping
- **Entities:** Earthquake Epicenter, Fault Line, Critical Infrastructure.
- **Relationships:** located_near, affects, detected_by.

## AI Readiness Assessment
- **Anomaly Detection:** Identify unusual seismic clusters.
- **Risk Modeling:** Correlate with building density (OSM) and soil type.
