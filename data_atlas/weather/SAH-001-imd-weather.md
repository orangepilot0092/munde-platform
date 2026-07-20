# SAH-001: IMD Weather Data

## Basic Information
- **Dataset ID:** SAH-001
- **Dataset Name:** IMD Real-time Weather Data
- **Description:** Real-time weather observations including temperature, humidity, wind speed, and rainfall from IMD stations across Maharashtra.
- **Domain:** Weather & Climate
- **Category:** Observational
- **Tags:** weather, imd, real-time, maharashtra

## Ownership
- **Department:** India Meteorological Department (IMD)
- **Data Owner:** IMD Pune
- **Publishing Organization:** Ministry of Earth Sciences
- **Official Website:** https://mausam.imd.gov.in/

## Source Information
- **Official URL:** https://api.imd.gov.in/
- **API Endpoint:** https://api.imd.gov.in/public/index.php
- **Documentation:** https://api.imd.gov.in/public/index.php
- **Authentication Method:** API Key (if required) / Public
- **Access Restrictions:** None for public endpoints

## Legal Information
- **License:** Open Government Data (OGD) License
- **Terms of Use:** Attribution required

## Update Information
- **Refresh Frequency:** Hourly / Daily
- **Historical Coverage:** Varies by station

## Technical Information
- **Format:** JSON / XML
- **Geographic Coverage:** 
  - State: Maharashtra
  - District: All
  - Latitude/Longitude Availability: Yes

## ETL Specification
- **Source Connector:** REST API
- **Download Strategy:** Polling every hour
- **Validation Rules:** Check for null values in temperature/rainfall
- **Storage Destination:** PostgreSQL (weather schema)

## AI Readiness Assessment
- **Forecasting:** High suitability for time-series models.
- **Anomaly Detection:** Suitable for extreme weather event detection.
