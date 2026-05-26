# =====================================================
# FILE: 02_PIPELINE_AND_CODE/orchestration/setup_gcp.py
# =====================================================

from google.cloud import storage, bigquery
from google.api_core import exceptions
from ..utilities import config

def initialize_gcp():
    storage_client = storage.Client(project=config.PROJECT_ID)
    bq_client = bigquery.Client(project=config.PROJECT_ID)

    # 1. Create Bucket
    bucket = storage_client.bucket(config.BUCKET_NAME)
    try:
        storage_client.create_bucket(bucket, location=config.LOCATION)
    except exceptions.Conflict: pass

    # 2. Create Dataset
    dataset = bigquery.Dataset(f"{config.PROJECT_ID}.{config.DATASET_ID}")
    dataset.location = config.LOCATION
    try:
        bq_client.create_dataset(dataset)
    except exceptions.Conflict: pass

    # 3. Create Bronze Table
    schema = [
        bigquery.SchemaField("source_file", "STRING"),
        bigquery.SchemaField("entity_type", "STRING"),
        bigquery.SchemaField("raw_value", "STRING"),
        bigquery.SchemaField("confidence", "FLOAT"),
        bigquery.SchemaField("extraction_timestamp", "TIMESTAMP"),
    ]
    table = bigquery.Table(f"{config.PROJECT_ID}.{config.DATASET_ID}.bronze_tax_data", schema=schema)
    try:
        bq_client.create_table(table)
        print("🚀 Infrastructure Ready.")
    except exceptions.Conflict: pass

if __name__ == "__main__":
    initialize_gcp()