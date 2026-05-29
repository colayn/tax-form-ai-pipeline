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
    
    # Process local files
    for filename in os.listdir(config.LOCAL_DATA_DIR):
        if filename.endswith(".pdf"):
            print(f"📄 AI Processing: {filename}...")
            with open(os.path.join(config.LOCAL_DATA_DIR, filename), "rb") as f:
                content = f.read()
                # Document AI call
                entities = extract_entities.process_document(content, filename)
                
                for ent in entities:
                    all_extracted_data.append({
                        "source_file": filename,
                        "entity_type": ent.type_,
                        "raw_value": ent.mention_text,
                        "confidence": round(ent.confidence, 2),
                        "extraction_timestamp": pd.Timestamp.now()
                    })

    if not all_extracted_data:
        print("⚠️ No data extracted. Check your PDF directory.")
        return

    # Load to BigQuery BRONZE Layer
    bronze_df = pd.DataFrame(all_extracted_data) 
    # CRITICAL: Point to the Bronze Dataset defined in your config
    table_id = f"{config.PROJECT_ID}.{config.BRONZE_DATASET}.bronze_tax_data"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", # Refreshes the raw layer
    )   
    print(f"📤 Uploading {len(bronze_df)} entities to {config.BRONZE_DATASET}...")
    job = bq_client.load_table_from_dataframe(bronze_df, table_id, job_config=job_config)
    job.result() # Wait for upload to finish
    
    # Save local checkpoint for debugging
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    bronze_df.to_csv(f"{config.OUTPUT_DIR}/sample_parsing_results.csv", index=False)
    
    print(f"🏁 RAW Data loaded to BRONZE. Proceed to 'dbt run' for Silver/Gold transformations.")

if __name__ == "__main__":
    run_main()
