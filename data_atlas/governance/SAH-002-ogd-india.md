# SAH-002: Open Government Data (OGD) Platform India

## Basic Information
- **Dataset ID:** SAH-002
- **Dataset Name:** OGD India - Maharashtra State Datasets
- **Description:** A centralized repository of machine-readable datasets published by various Ministries/Departments of the Government of India and State Governments, including Maharashtra.
- **Domain:** Multi-Domain (Governance, Agriculture, Water, Energy)
- **Category:** Aggregated Portal
- **Tags:** ogd, open-data, maharashtra, government

## Ownership
- **Department:** Ministry of Electronics and Information Technology (MeitY)
- **Data Owner:** Various State/Central Departments
- **Publishing Organization:** National Informatics Centre (NIC)
- **Official Website:** https://data.gov.in/

## Source Information
- **Official URL:** https://data.gov.in/
- **API Endpoint:** https://api.data.gov.in/resource/
- **Documentation:** https://docs.ogdp.gov.in/
- **Authentication Method:** API Key (Required for high-volume access)
- **Access Restrictions:** Public; some datasets may have specific licensing terms.

## Legal Information
- **License:** Open Government Data (OGD) License India v2.0
- **Terms of Use:** Attribution required; non-commercial and commercial use permitted.

## Update Information
- **Refresh Frequency:** Varies by dataset (Daily/Monthly/Annual)
- **Historical Coverage:** Extensive (varies by source department)

## Technical Information
- **Format:** JSON, CSV, XML
- **Geographic Coverage:** 
  - State: Maharashtra (and all other states)
  - District: All
  - Latitude/Longitude Availability: Yes (for geospatial datasets)

## ETL Specification
- **Source Connector:** REST API / Bulk Download
- **Download Strategy:** Metadata-first discovery, then targeted ingestion of Maharashtra-specific resources.
- **Validation Rules:** Verify state code ('MH') in metadata.
- **Storage Destination:** PostgreSQL (domain-specific schemas)

## AI Readiness Assessment
- **Classification:** High suitability for training models on government schemes and demographics.
- **RAG:** Excellent source for policy and scheme documentation.
