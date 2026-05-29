# =====================================================
# FILE: utilities/config.py
# =====================================================

# Global Settings
PROJECT_ID = "fgh-ds-practical-497509" # <--- Modify - Click your Project. Copy the ID
LOCATION = "us"
PROCESSOR_ID = "2f71eeb60480ad05" # <--- Modify
BUCKET_NAME = f"{PROJECT_ID}-tax-pipeline"
# DATASET_ID = "tax_pipeline_db"

# NEW
BRONZE_DATASET = "bronze_raw_extractions"
SILVER_DATASET = "silver_clean_transformations"
GOLD_DATASET   = "gold_mart_crm"

# Local Paths
LOCAL_DATA_DIR = "01_DATA_SOURCES/sampling_input_docs"
OUTPUT_DIR = "05_SAMPLE_OUTPUTS"
