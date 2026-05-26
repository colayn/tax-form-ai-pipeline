from google.cloud import storage
import os
from ..utilities import config

def upload_local_documents():
    client = storage.Client(project=config.PROJECT_ID)
    bucket = client.bucket(config.BUCKET_NAME)
    
    for filename in os.listdir(config.LOCAL_DATA_DIR):
        if filename.endswith(".pdf"):
            blob = bucket.blob(f"input_docs/{filename}")
            blob.upload_from_filename(os.path.join(config.LOCAL_DATA_DIR, filename))
            print(f"✅ Uploaded {filename} to GCS.")

if __name__ == "__main__":
    upload_local_documents()