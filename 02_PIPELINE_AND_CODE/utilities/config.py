# =====================================================
# FILE: utilities/config.py
# =====================================================

# Global Settings
PROJECT_ID = "YOUR_PROJECT_ID" # <--- Modify - Click your Project. Copy the ID
LOCATION = "us"
PROCESSOR_ID = "YOUR_DOCUMENT_AI_PROCESSOR_ID" # <--- Modify
BUCKET_NAME = f"{PROJECT_ID}-tax-pipeline"
DATASET_ID = "tax_pipeline_db"

# Local Paths
LOCAL_DATA_DIR = "01_DATA_SOURCES/sampling_input_docs"
OUTPUT_DIR = "01_DATA_SOURCES/output_checkpoints"
