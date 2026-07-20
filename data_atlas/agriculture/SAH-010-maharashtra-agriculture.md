# SAH-010: Maharashtra Agriculture Statistics & APMC Prices

## Basic Information
- **Dataset ID:** SAH-010
- **Dataset Name:** APMC Daily Prices & Crop Sowing Status
- **Description:** Daily arrival and price data from Agricultural Produce Market Committees (APMCs) across Maharashtra, along with weekly crop sowing progress reports.
- **Domain:** Agriculture
- **Category:** Market Data / Operational
- **Tags:** agriculture, apmc, prices, crops, krishisetu, market

## Ownership
- **Department:** Department of Agriculture, Govt. of Maharashtra
- **Data Owner:** Director of Agriculture
- **Publishing Organization:** Govt. of Maharashtra
- **Official Website:** https://mahadbtagriculture.in/

## Source Information
- **Official URL:** https://apmc.maharashtra.gov.in/
- **API Endpoint:** Available via OGD India (SAH-002) or direct portal scraping.
- **Documentation:** https://data.gov.in/
- **Authentication Method:** Public
- **Access Restrictions:** None

## Legal Information
- **License:** Open Government Data (OGD) License
- **Terms of Use:** Attribution required.

## Update Information
- **Refresh Frequency:** Daily (Prices), Weekly (Sowing)
- **Historical Coverage:** Last 10+ years

## Technical Information
- **Format:** HTML Table / CSV / Excel
- **Geographic Coverage:** 
  - State: Maharashtra
  - Market: All APMCs (e.g., Pune, Lasalgaon, Sangli)

## ETL Specification
- **Source Connector:** HTML Parser / API Client
- **Download Strategy:** Daily poll for top 20 markets; weekly bulk update for sowing.
- **Validation Rules:** Verify price ranges against historical averages to detect outliers.
- **Storage Destination:** PostgreSQL (agriculture schema)

## AI Readiness Assessment
- **Forecasting:** Predict price trends for major crops (Onion, Soybean, Cotton).
- **Recommendation Systems:** Advise farmers on best markets to sell produce based on real-time prices.
