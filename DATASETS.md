# Project Sahyadri — Data Foundation

## Acquired Sovereign Datasets
The following high-value, open-source AI4Bharat datasets have been successfully downloaded and are stored locally at `/mnt/d/sahyadri-data/datasets/indic_starter/`. They are excluded from Git to preserve repository size and data sovereignty.

1. **`ai4bharat/naamapadam`** (360 MB)  
   - **Purpose:** Named Entity Recognition (NER) for Indian languages.  
   - **Sahyadri Use Case:** Crucial for extracting names, locations, and government scheme identifiers from unstructured documents (GRs, circulars).

2. **`ai4bharat/indic_glue`** (602 MB)  
   - **Purpose:** The gold-standard benchmark for evaluating Indian language NLP models.  
   - **Sahyadri Use Case:** Continuous evaluation and benchmarking of our sovereign LLMs to ensure >95% accuracy.

3. **`ai4bharat/indic-instruct-data-v0.1`** (739 MB)  
   - **Purpose:** Instruction-tuning data for Indian languages.  
   - **Sahyadri Use Case:** Fine-tuning base models to follow complex, multilingual government policy queries accurately in Marathi and Hindi.

## Data Governance
- **Storage:** Local 2TB NVMe (`/mnt/d/`) for PC Node ETL; replicated to DGX Spark AI Node for training.
- **Access:** Managed via MinIO object storage in production.
- **Compliance:** All datasets are open-source and align with India's Open Government Data (OGD) principles.
