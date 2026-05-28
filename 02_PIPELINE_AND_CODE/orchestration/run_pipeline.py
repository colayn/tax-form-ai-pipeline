# =====================================================
# FILE: orchestration/run_pipeline.py
# =====================================================

import os
import pandas as pd
from google.cloud import bigquery
from ..ingestion import extract_entities
from ..utilities import config

def run_main():
    bq_client = bigquery.Client(project=config.PROJECT_ID)
    all_extracted_data = []
    
    for filename in os.listdir(config.LOCAL_DATA_DIR):
        if filename.endswith(".pdf"):
            print(f"📄 Processing: {filename}...") # Add this line
            with open(os.path.join(config.LOCAL_DATA_DIR, filename), "rb") as f:
                entities = extract_entities.process_document(f.read(), filename)
                for ent in entities:
                    all_extracted_data.append({
                        "source_file": filename,
                        "entity_type": ent.type_,
                        "raw_value": ent.mention_text,
                        "confidence": round(ent.confidence, 2),
                        "extraction_timestamp": pd.Timestamp.now()
                    })

    # Load to BigQuery Bronze
    bronze_df = pd.DataFrame(all_extracted_data)
    table_id = f"{config.PROJECT_ID}.{config.DATASET_ID}.bronze_tax_data"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    bq_client.load_table_from_dataframe(bronze_df, table_id, job_config=job_config).result()
    
    # Save local checkpoint
    bronze_df.to_csv(f"{config.OUTPUT_DIR}/bronze_checkpoint.csv", index=False)
    print("🏁 Python Pipeline Finished. Now run 'dbt run'.")

if __name__ == "__main__":
    run_main()
