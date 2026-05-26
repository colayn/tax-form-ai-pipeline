# =====================================================
# FILE: ingestion/extract_entities.py
# =====================================================
# =====================================================
# PURPOSE
# =====================================================
# This module sends sampled PDF tax forms to
# Google Document AI W-2 Parser for entity extraction.
#
# Extracted entities and confidence scores are
# serialized into JSON outputs for downstream
# medallion transformations.
#
# PIPELINE STAGE:
# AI Extraction
#
# OUTPUT:
# output/json/
# =====================================================

from google.cloud import documentai_v1 as documentai
from google.cloud import storage
import json
from ..utilities import config

def process_document(file_content, filename):
    # 1. Call DocAI
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(config.PROJECT_ID, config.LOCATION, config.PROCESSOR_ID)
    raw_document = documentai.RawDocument(content=file_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    
    # 2. Save Raw JSON to Bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(config.BUCKET_NAME)
    json_blob = bucket.blob(f"bronze_json/{filename.replace('.pdf', '.json')}")
    json_blob.upload_from_string(documentai.Document.to_json(result.document))
    
    return result.document.entities