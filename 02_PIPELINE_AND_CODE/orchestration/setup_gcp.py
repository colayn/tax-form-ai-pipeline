# =====================================================
# FILE: 02_PIPELINE_AND_CODE/orchestration/setup_gcp.py
# =====================================================

from google.cloud import storage, bigquery
from google.api_core import exceptions
from ..utilities import config

def initialize_gcp():
    storage_client = storage.Client(project=config.PROJECT_ID)
    bq_client = bigquery.Client(project=config.PROJECT_ID)

    # 1. Create Bucket (Landing Zone)
    bucket = storage_client.bucket(config.BUCKET_NAME)
    try:
        storage_client.create_bucket(bucket, location=config.LOCATION)
        print(f"✅ Bucket {config.BUCKET_NAME} created.")
    except exceptions.Conflict: pass

    # 2. Create the 3 Medallion Datasets
    datasets = [config.BRONZE_DATASET, config.SILVER_DATASET, config.GOLD_DATASET]
    
    for ds_id in datasets:
        dataset = bigquery.Dataset(f"{config.PROJECT_ID}.{ds_id}")
        dataset.location = config.LOCATION
        try:
            bq_client.create_dataset(dataset)
            print(f"✅ Dataset {ds_id} created.")
        except exceptions.Conflict: pass

    # 3. Create Bronze Table (Strictly in the Bronze Dataset)
    schema = [
        bigquery.SchemaField("source_file", "STRING"),
        bigquery.SchemaField("entity_type", "STRING"),
        bigquery.SchemaField("raw_value", "STRING"),
        bigquery.SchemaField("confidence", "FLOAT"),
        bigquery.SchemaField("extraction_timestamp", "TIMESTAMP"),
    ]
    # BRONZE_DATASET
    table_id = f"{config.PROJECT_ID}.{config.BRONZE_DATASET}.bronze_tax_data"
    table = bigquery.Table(table_id, schema=schema)
    
    try:
        bq_client.create_table(table)
        print(f"🚀 Infrastructure Ready. Bronze table created at: {table_id}")
    except exceptions.Conflict: pass

if __name__ == "__main__":
    initialize_gcp()
