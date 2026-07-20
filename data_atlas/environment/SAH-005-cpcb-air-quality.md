# SAH-005: CPCB Real-time Air Quality Data

## Basic Information
- **Dataset ID:** SAH-005
- **Dataset Name:** Central Pollution Control Board (CPCB) AQI
- **Description:** Real-time air quality data from Continuous Ambient Air Quality Monitoring Stations (CAAQMS) across Maharashtra. Includes parameters like PM2.5, PM10, NO2, SO2, CO, O3, NH3, and Pb.
- **Domain:** Environment / Health
- **Category:** Time-Series / Observational
- **Tags:** air-quality, aqi, cpcb, pollution, health, real-time

## Ownership
- **Department:** Central Pollution Control Board (CPCB)
- **Data Owner:** Ministry of Environment, Forest and Climate Change
- **Publishing Organization:** CPCB
- **Official Website:** https://cpcb.nic.in/

## Source Information
- **Official URL:** https://app.cpcbccr.com/ccr/
- **API Endpoint:** https://api.data.gov.in/resource/ (via OGD India) or direct scraping if API is unstable.
- **Documentation:** https://cpcb.nic.in/air-quality-data/
- **Authentication Method:** Public / API Key (via OGD)
- **Access Restrictions:** None for public data.

## Legal Information
- **License:** Open Government Data (OGD) License
- **Terms of Use:** Attribution required.

## Update Information
- **Refresh Frequency:** Hourly
- **Historical Coverage:** Varies by station (some since 2015)

## Technical Information
- **Format:** JSON / CSV
- **Geographic Coverage:** 
  - State: Maharashtra
  - Cities: Mumbai, Pune, Nagpur, Nashik, Aurangabad, etc.
  - Latitude/Longitude Availability: Yes

## ETL Specification
- **Source Connector:** REST API (OGD) or HTML Parser (fallback)
- **Download Strategy:** Poll every hour for latest readings.
- **Validation Rules:** Check for negative values or impossible AQI spikes.
- **Storage Destination:** PostgreSQL (environment schema)

## AI Readiness Assessment
- **Forecasting:** High suitability for predicting AQI trends based on weather and traffic.
- **Anomaly Detection:** Identify sudden pollution events (e.g., stubble burning impact).
- **Clustering:** Group cities with similar pollution profiles.
