#!/bin/bash

# =====================================================
# PURPOSE
# =====================================================
# Master orchestration script for the
# Tax Form AI Pipeline on Google Cloud Platform.
#
# This script automates:
# - Infrastructure setup
# - PDF ingestion
# - Document AI extraction
# - Bronze/Silver/Gold transformations
# - dbt validation testing
#
# OUTPUT:
# CRM-ready Gold Layer in BigQuery
# =====================================================

# Exit immediately if a command fails
set -e

# =====================================================
# ERROR HANDLER
# =====================================================

handle_error() {

    echo ""
    echo "❌ PIPELINE FAILED"
    echo "Failed at step:"
    echo "$1"
    echo ""

    exit 1
}

# =====================================================
# START PIPELINE
# =====================================================

echo ""
echo "=================================================="
echo "🚀 STARTING TAX-TO-CRM AI DATA PIPELINE"
echo "=================================================="
echo ""

START_TIME=$(date)

echo "🕒 Start Time: $START_TIME"

# =====================================================
# STEP 1 — GCP SETUP
# =====================================================

echo ""
echo "☁️ Setting up GCP Infrastructure..."

python3 -m 02_PIPELINE_AND_CODE.orchestration.setup_gcp \
|| handle_error "GCP Infrastructure Setup"

# =====================================================
# STEP 2 — UPLOAD PDFs TO GCS
# =====================================================

echo ""
echo "📂 Uploading PDFs to GCS..."

python3 -m 02_PIPELINE_AND_CODE.ingestion.upload_to_gcs \
|| handle_error "GCS Upload"

# =====================================================
# STEP 3 — DOCUMENT AI EXTRACTION
# =====================================================

echo ""
echo "🤖 Running Document AI Extraction..."

python3 -m 02_PIPELINE_AND_CODE.orchestration.run_pipeline \
|| handle_error "Document AI Extraction"

# =====================================================
# STEP 4 — DBT TRANSFORMATIONS
# =====================================================

echo ""
echo "💎 Running dbt Transformations..."

cd 03_DBT_TRANSFORMATIONS \
|| handle_error "dbt Directory Navigation"

# =====================================================
# STEP 6 — DBT DEBUG
# =====================================================

echo ""
echo "🔍 Validating dbt Configuration..."

dbt debug || handle_error "dbt debug"

# =====================================================
# STEP 5 — DBT RUN
# =====================================================

echo ""
echo "🔄 Executing dbt run..."

dbt run || handle_error "dbt run"

# =====================================================
# STEP 6 — DBT TEST
# =====================================================

echo ""
echo "🧪 Executing dbt tests..."

dbt test || handle_error "dbt test"

# =====================================================
# PIPELINE COMPLETE
# =====================================================

END_TIME=$(date)

echo ""
echo "=================================================="
echo "✅ PIPELINE COMPLETED SUCCESSFULLY"
echo "=================================================="
echo ""

echo "🕒 Start Time: $START_TIME"
echo "🕒 End Time:   $END_TIME"

echo ""
echo "🥇 Gold Layer is ready in BigQuery. Gold Table: gold_crm_ready_data"
echo ""