# 🧾 Tax Form AI Pipeline on Google Cloud Platform (GCP)

An automated Intelligent Document Processing (IDP) pipeline that extracts structured customer information from unstructured W-2 tax form PDFs using Google Document AI, Medallion Architecture, dbt transformations, and BigQuery.

---

# 🚀 Business Problem

The Sales Operations team receives scanned PDF copies of tax forms from new retail customers. Currently, personnel manually review each document and encode customer information into the CRM system, resulting in a time-consuming and error-prone process due to the high monthly document volume.

To improve operational efficiency, this project implements an automated AI-powered data pipeline on Google Cloud Platform (GCP) capable of extracting critical customer information from unstructured tax documents and transforming it into structured, CRM-ready datasets.

---

# 🏗️ Solution Overview

This project delivers:

✅ Automated PDF ingestion pipeline
✅ AI-powered entity extraction using Document AI
✅ Medallion Architecture (Bronze → Silver → Gold)
✅ Confidence-based validation rules
✅ dbt warehouse transformations
✅ BigQuery warehouse loading
✅ Reproducible and modular pipeline orchestration

---

# ☁️ GCP Services Used

| Service                    | Purpose                       |
| -------------------------- | ----------------------------- |
| Google Cloud Storage (GCS) | PDF landing bucket            |
| Google Document AI         | W-2 tax form extraction       |
| BigQuery                   | Data warehouse                |
| dbt                        | Silver & Gold transformations |
| Python                     | Orchestration & ETL           |

---

# 🏛️ Pipeline Architecture

```text
Retail Customer PDFs
        │
        ▼
Google Cloud Storage (GCS)
   "Landing Bucket"
        │
        ▼
run_pipeline.py
(Orchestration Layer)
        │
        ▼
Google Document AI
(W-2 Parser)
        │
        ▼
Raw JSON Extraction
(output/json)
        │
        ▼
🥉 Bronze Layer
bronze_raw_extractions
(BigQuery)
        │
        ▼
dbt Silver Model
stg_silver_tax_forms.sql
        │
        ▼
🥈 Silver Layer
silver_clean_tax_forms
(BigQuery)
        │
        ▼
dbt Gold Model
gold_tax_forms_crm.sql
        │
        ▼
🥇 Gold Layer
gold_crm_ready_data
(BigQuery)
        │
        ▼
CRM / BI Dashboard
```

---

# 🥉 Bronze Layer

## Purpose

Stores raw extracted entities directly from Google Document AI.

## Characteristics

* Preserves raw extraction outputs
* Maintains confidence scores
* Supports traceability and auditability
* One row per extracted entity

## Schema

| Column               | Description            |
| -------------------- | ---------------------- |
| source_file          | Original PDF filename  |
| entity_type          | Extracted entity label |
| raw_value            | Raw extracted value    |
| confidence           | AI confidence score    |
| extraction_timestamp | Extraction timestamp   |

---

# 🥈 Silver Layer

## Purpose

Transforms raw extraction outputs into cleaned and validated customer records.

## Transformations

* Entity standardization
* Confidence score computation
* Missing field validation
* Review flagging
* Data quality checks

## Validation Rules

| Rule              | Action                  |
| ----------------- | ----------------------- |
| Missing SSN       | review_required = TRUE  |
| Low confidence    | review_required = TRUE  |
| Passed validation | review_required = FALSE |

## Schema

| Column                  | Description                 |
| ----------------------- | --------------------------- |
| source_file             | Original PDF                |
| employee_first_name     | Employee first name         |
| employee_last_name      | Employee last name          |
| employee_ssn            | Employee SSN                |
| employee_street_address | Employee address            |
| employee_city           | City                        |
| employee_state          | State                       |
| confidence_score        | Minimum critical confidence |
| review_required         | Manual review flag          |
| review_reason           | Validation issue            |

---

# 🥇 Gold Layer

## Purpose

Provides trusted CRM-ready customer records for downstream operational systems.

## Gold Filtering Logic

Only validated records satisfying:

```sql
review_required = FALSE
```

are promoted into the Gold layer.

## Consumption Targets

* CRM systems
* Business Intelligence dashboards
* Operational analytics
* Customer onboarding workflows

---

# 🎲 Dataset Sampling Strategy

The original dataset consisted of 250 W-2 PDF documents.

To maintain repository portability and reproducibility, a representative subset of 50 PDFs was selected using deterministic random sampling with a fixed random seed.

Sampling script:

```text
02_PIPELINE_AND_CODE/ingestion/random_sampling.py
```

---

# 📂 Repository Structure

```text
tax-form-ai-pipeline
│
├── 01_DATA_SOURCES/
│   └── sampling_input_docs/
│
├── 02_PIPELINE_AND_CODE/
│   ├── ingestion/
│   │   ├── extract_entities.py
│   │   ├── random_sampling.py
│   │   └── upload_to_gcs.py
│   │
│   ├── orchestration/
│   │   ├── run_pipeline.py
│   │   └── setup_gcp.py
│   │
│   ├── transformation/
│   │
│   └── utilities/
│       └── config.py
│
├── 03_DBT_TRANSFORMATIONS/
│   ├── models/
│   │   ├── clean/
|   |   |   ├── silver_clean_tax_forms.sql 
│   |   |   └── schema.yml
│   |   |
│   │   └── mart/
|   |       ├── gold_crm_ready_data.sql
│   |       └── schema.yml
│   │
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── 04_DATA_MODEL/
│
├── 05_ANALYSIS_AND_REPORTS/
│
├── README.md
└── requirements.txt
```

---

# ⚙️ Environment Setup

## 1. Clone Repository

```bash
git clone <your-github-repository>

cd tax-form-ai-pipeline
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 GCP Authentication

## Initialize GCloud

```bash
gcloud init
```

---

## Authenticate Application Default Credentials

```bash
gcloud auth application-default login
```

---

# ☁️ Enable Required APIs

```bash
gcloud services enable documentai.googleapis.com

gcloud services enable storage.googleapis.com

gcloud services enable bigquery.googleapis.com
```

---

# 🏗️ Infrastructure Setup

Run:

```bash
python3 -m 02_PIPELINE_AND_CODE.orchestration.setup_gcp
```

This automatically provisions:

✅ GCS Bucket
✅ BigQuery Dataset
✅ Warehouse Tables

---

# 🚀 Running the End-to-End Pipeline

Run the orchestrated pipeline:

```bash
python3 -m 02_PIPELINE_AND_CODE.orchestration.run_pipeline
```

Pipeline stages:

1. Random Sampling
2. Upload PDFs to GCS
3. Document AI Extraction
4. Bronze Layer Generation
5. BigQuery Loading
6. dbt Silver Transformation
7. dbt Gold Transformation

---

# 💎 Running dbt Transformations

Navigate to:

```bash
cd 03_DBT_TRANSFORMATIONS
```

Run:

```bash
dbt debug

dbt run

dbt test
```

---

# 🔍 Traceability & Governance

The Medallion Architecture enables full lineage tracing:

```text
Gold → Silver → Bronze → Raw PDF
```

This supports:

* auditability
* debugging
* extraction validation
* operational governance
* confidence monitoring

---

# 📊 Confidence Threshold Strategy

The pipeline implements confidence-based validation to improve CRM data quality.

Low-confidence or incomplete records are flagged for manual review before promotion into downstream systems.

---

# 🚧 Known Limitations

* Legacy 2010 W-2 layouts occasionally miss city/state extraction
* Pretrained W-2 Parser may underperform on noisy scans
* Manual review still required for low-confidence records

---

# 🔮 Future Improvements

* Event-driven GCS triggers
* Cloud Composer orchestration
* Real-time streaming ingestion
* Custom Document AI processor training
* CRM API integration
* CI/CD deployment pipeline

---

# 👨‍💻 Author

Developed as part of a GCP Data Engineering & AI Pipeline practical assessment.
