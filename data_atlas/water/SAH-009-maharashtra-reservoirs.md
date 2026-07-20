# SAH-009: Maharashtra Reservoir Daily Status

## Basic Information
- **Dataset ID:** SAH-009
- **Dataset Name:** Maharashtra Major & Medium Reservoirs Daily Status
- **Description:** Daily water storage levels, live capacity, and inflow/outflow data for major and medium dams across Maharashtra. Critical for drought monitoring and irrigation planning.
- **Domain:** Water Resources
- **Category:** Time-Series / Operational
- **Tags:** water, reservoir, dam, irrigation, jalsetu, daily

## Ownership
- **Department:** Water Resources Department (WRD), Government of Maharashtra
- **Data Owner:** Executive Engineer, WRD
- **Publishing Organization:** Govt. of Maharashtra
- **Official Website:** https://maha-water.gov.in/

## Source Information
- **Official URL:** https://maha-water.gov.in/ (Daily Reports Section)
- **API Endpoint:** None (Currently PDF/Excel)
- **Documentation:** Internal WRD manuals
- **Authentication Method:** Public
- **Access Restrictions:** None

## Legal Information
- **License:** Open Government Data (OGD) License
- **Terms of Use:** Attribution required.

## Update Information
- **Refresh Frequency:** Daily (usually by 10:00 AM)
- **Historical Coverage:** Last 5–10 years (archived)

## Technical Information
- **Format:** PDF / Excel (.xlsx)
- **Geographic Coverage:** 
  - State: Maharashtra
  - District: All
  - River Basin: Godavari, Krishna, Narmada, Tapi

## ETL Specification
- **Source Connector:** Web Scraper / PDF Parser
- **Download Strategy:** Daily fetch of the "Daily Water Stock" report.
- **Validation Rules:** Check for total capacity consistency; flag negative inflows.
- **Storage Destination:** PostgreSQL (water schema)

## AI Readiness Assessment
- **Forecasting:** High suitability for predicting reservoir depletion rates.
- **Anomaly Detection:** Identify sudden drops in levels indicating leaks or unauthorized release.
