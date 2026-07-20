# SAH-004: Copernicus Sentinel-2 Imagery

## Basic Information
- **Dataset ID:** SAH-004
- **Dataset Name:** Sentinel-2 MSI Level-1C/2A
- **Description:** High-resolution optical imagery for land monitoring. Provides 13 spectral bands at 10m, 20m, and 60m resolution. Critical for crop health (NDVI), water body mapping, and urban expansion tracking.
- **Domain:** Environment / Agriculture
- **Category:** Satellite Imagery
- **Tags:** sentinel-2, copernicus, ndvi, earth-observation, optical

## Ownership
- **Department:** European Space Agency (ESA)
- **Data Owner:** ESA / Copernicus Programme
- **Publishing Organization:** European Commission
- **Official Website:** https://sentinel.esa.int/web/sentinel/missions/sentinel-2

## Source Information
- **Official URL:** https://scihub.copernicus.eu/
- **API Endpoint:** https://dataspace.copernicus.eu/ (New Data Space API)
- **Documentation:** https://documentation.dataspace.copernicus.eu/
- **Authentication Method:** OAuth2 (Keycloak)
- **Access Restrictions:** Free and Open.

## Legal Information
- **License:** Copernicus Data License
- **Terms of Use:** Free for all users.

## Update Information
- **Refresh Frequency:** 5 days (revisit time with two satellites)
- **Historical Coverage:** Since 2015

## Technical Information
- **Format:** JPEG2000 (within SAFE structure)
- **Spatial Reference System:** UTM/WGS84
- **Geographic Coverage:** Global (including all of Maharashtra)

## ETL Specification
- **Source Connector:** Copernicus Data Space Ecosystem API
- **Download Strategy:** Query by bounding box (Maharashtra) and cloud cover percentage (<10%).
- **Validation Rules:** Check for missing bands or corrupted tiles.
- **Storage Destination:** MinIO (Raw .SAFE files), PostgreSQL (Metadata)

## AI Readiness Assessment
- **Computer Vision:** Primary input for crop classification, yield prediction, and flood mapping.
- **Change Detection:** Ideal for monitoring urban sprawl or deforestation over time.
