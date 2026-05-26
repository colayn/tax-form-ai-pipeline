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

# 🏛️ Pipeline Architecture


![alt text](pipeline-architecture-1.png)


---

# 🥉 Bronze Layer

## Purpose

Stores raw extracted entities directly from Google Document AI.

## Characteristics

- Preserves raw extraction outputs
- Maintains confidence scores
- Supports traceability and auditability
- One row per extracted entity

## Schema

| Column | Description |
|---|---|
| source_file | Original PDF filename |
| entity_type | Extracted entity label |
| raw_value | Raw extracted value |
| confidence | AI confidence score |
| extraction_timestamp | Extraction timestamp |

---

# 🥈 Silver Layer

## Purpose

Transforms raw extraction outputs into cleaned and validated customer records.

## Transformations

- Entity standardization
- Confidence score computation
- Missing field validation
- Review flagging
- Data quality checks

## Validation Rules

| Rule | Action |
|---|---|
| Missing SSN | review_required = TRUE |
| Low confidence | review_required = TRUE |
| Passed validation | review_required = FALSE |

## Schema

| Column | Description |
|---|---|
| source_file | Original PDF |
| employee_first_name | Employee first name |
| employee_last_name | Employee last name |
| employee_ssn | Employee SSN |
| employee_street_address | Employee address |
| employee_city | City |
| employee_state | State |
| confidence_score | Minimum critical confidence |
| review_required | Manual review flag |
| review_reason | Validation issue |

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

---

# 🎲 Dataset Sampling Strategy

The original dataset consisted of 250 W-2 PDF documents.

To maintain repository portability and reproducibility, a representative subset of 50 PDFs was selected using deterministic random sampling with a fixed random seed.

Sampling script:

```text
02_PIPELINE_AND_CODE/ingestion/random_sampling.py
```
Random sampling subset location:

```text
├── 01_DATA_SOURCES/
│   └── sampling_input_docs/
```

---

# 📂 Repository Structure

```text
tax-form-ai-pipeline
│
├── 01_DATA_SOURCES/
│   └── sampling_input_docs/    # Input PDF samples
│
├── 02_PIPELINE_AND_CODE/       # Python Orchestration
│   ├── ingestion/              # GCS Upload & PDF processing
│   │   ├── extract_entities.py
│   │   ├── random_sampling.py
│   │   └── upload_to_gcs.py
│   │
│   ├── orchestration/          # GCP Setup & Document AI
│   │   ├── run_pipeline.py
│   │   └── setup_gcp.py
│   │
│   └── utilities/              # Configuration
│       └── config.py
│
├── 03_DBT_TRANSFORMATIONS/     # SQL Transformation Layer
│   ├── models/
│   │   ├── clean/              # Silver Layer (Validation & Pivoting)
|   |   |   ├── silver_clean_tax_forms.sql 
│   |   |   └── schema.yml
│   |   |
│   │   └── mart/               # Gold Layer (Business Aliasing)
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

# ☁️ GCP Services Used

| Service | Purpose |
|---|---|
| Google Cloud Storage (GCS) | PDF landing bucket |
| Google Document AI | W-2 tax form extraction |
| BigQuery | Data warehouse |
| dbt | Silver & Gold transformations |
| Python | Orchestration & ETL |

---

# 💻 Recommended Execution Environment

This project is designed to run inside:

- Google Cloud Shell
- Google Cloud Console
- GCP-enabled Linux environments

Running inside Google Cloud Shell is recommended because it provides:

✅ Pre-installed gcloud SDK  
✅ Native GCP authentication  
✅ Simplified BigQuery access  
✅ Built-in Python environment  
✅ Reduced local environment setup issues  

---

# ⚙️ Environment Setup

## 1. Create or Select a GCP Project

Inside Google Cloud Console:

```text
Google Cloud Console
→ Select/Create Project
```

Enable billing for the project.

---

## 2. Launch Google Cloud Shell

```text
Google Cloud Console
→ Activate Cloud Shell
```

---

## 3. Clone Repository

```bash
git clone https://github.com/colayn/tax-form-ai-pipeline.git

cd tax-form-ai-pipeline
```

---

## 4. Create Virtual Environment

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip3 install -r requirements.txt
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

# 🤖 Create Document AI W-2 Processor

This project uses the pretrained Google Document AI:

```text
W-2 Parser
```

for tax form entity extraction.

---

## Steps

1. Open Google Cloud Console

2. Navigate to:

```text
Document AI → Explore Processors
```
3. Select:

```text
Specialized Processors
→ W-2 Parser
```

4. Click:

```text
Create Processor -> Processor name: <your-processor-name> -> Region: US -> Create
```

5. Choose:

```text
Go to Manage Version -> 
Select Version:
pretrained-w2-v2.0-2022-03-30
-> Set as default
```

---

## Retrieve Processor ID

After creation:

```text
Document AI
→ My Processors
→ Select W-2 Parser
```

Copy the:

```text
Processor ID
```

Example:

```text
5aabab6dc13ee5cc
```

---

## Update Configuration

Open:

```text
Open Editor (VSCode Editor in GCP) 

02_PIPELINE_AND_CODE/utilities/config.py
```

Update:

```python
PROJECT_ID = "YOUR_PROJECT_ID" # Click your Project. Copy the ID
PROCESSOR_ID = "YOUR_DOCUMENT_AI_PROCESSOR_ID"
```

## Update DBT Transformations

Open:

```text 
03_DBT_TRANSFORMATIONS/profiles.yml
```

Update:

```python
project: <YOUR_PROJECT_ID> # Click your Project. Copy the ID
```
Open:

```text 
03_DBT_TRANSFORMATIONS/models/clean/schema.yml
```

Update:

```python
project: <YOUR_PROJECT_ID> # Click your Project. Copy the ID
```


---

# 🚀 Running the End-to-End Pipeline

Run the orchestrated pipeline:

```bash
Click Open Terminal

chmod +x run_tax_form_pipeline.sh

./run_tax_form_pipeline.sh
```

Prompt upon completing the pipeline:

```bash
==================================================
✅ PIPELINE COMPLETED SUCCESSFULLY
==================================================

🕒 Start Time: Tue May 26 10:47:32 AM UTC 2026
🕒 End Time:   Tue May 26 10:55:27 AM UTC 2026

🥇 Gold Layer is ready in BigQuery. Gold Table: gold_crm_ready_dat
```


### Pipeline stages:

1. Random Sampling
2. Upload PDFs to GCS
3. Document AI Extraction
4. Bronze Layer Generation
5. BigQuery Loading
6. dbt Silver Transformation
7. dbt Gold Transformation

---

# 🔍 Traceability & Governance

The Medallion Architecture enables full lineage tracing:

```text
Gold → Silver → Bronze → Raw PDF
```

This supports:

- auditability
- debugging
- extraction validation
- operational governance
- confidence monitoring

---

# 📊 Confidence Threshold Strategy

The pipeline implements confidence-based validation to improve CRM data quality.

Low-confidence or incomplete records are flagged for manual review before promotion into downstream systems.

---

# 🚧 Known Limitations

- Legacy 2010 W-2 layouts occasionally miss city/state extraction
- Pretrained W-2 Parser may underperform on noisy scans
- Manual review still required for low-confidence records

---

# 🔮 Future Improvements

- Event-driven GCS triggers
- Cloud Composer orchestration
- Real-time streaming ingestion
- Custom Document AI processor training
- CRM API integration
- CI/CD deployment pipeline
- Cloud Run container deployment

---
