# 📑 AI-Powered Tax-to-CRM Data Pipeline

## 🌟 Project Overview
This project automates the extraction and transformation of unstructured retail customer tax forms (W-2s) into a structured format ready for CRM integration. By leveraging **GCP Document AI** and **dbt**, we have eliminated manual data entry, reduced human error, and implemented a robust "Quality Gate" to ensure only high-accuracy data reaches the final business layer.

## 🏗️ Technical Architecture: The Medallion Approach
The pipeline follows the **Medallion Architecture**, organizing data into three distinct layers of increasing quality:

* **Bronze (Raw):** Ingests raw AI output from Document AI into BigQuery.
* **Silver (Clean):** Pivots data into a relational schema and calculates a **Weighted Identity Confidence Score**.
* **Gold (Mart):** Applies business logic to alias fields (e.g., SSN to Customer ID) and filters out records failing the 70% quality threshold.


---

## 📂 Repository Structure
```text
tax-form-ai-pipeline/
├── 01_DATA_SOURCES/           # Input PDF samples
|   ├── sampling_input_docs/ 
├── 02_PIPELINE_AND_CODE/      # Python Orchestration
│   ├── ingestion/             # GCS Upload & PDF processing
│   ├── orchestration/         # GCP Setup & Document AI triggers
│   └── utilities/             # Configuration & logging
├── 03_DBT_TRANSFORMATIONS/    # SQL Transformation Layer
│   ├── models/
│   │   ├── clean/             # Silver Layer (Validation & Pivoting)
│   │   └── mart/              # Gold Layer (Business Aliasing)
│   └── dbt_project.yml        # dbt Configuration
├── 04_DATA_MODEL/             # Schema definitions
├── README.md                  # Project Documentation
└── requirements.txt           # Python dependencies