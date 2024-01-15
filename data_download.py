import os
import zipfile
from google.cloud import storage

key_file_path = "key_service_account.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path

storage_client = storage.Client()
bucket = storage_client.bucket("smoke_detection")
blob = bucket.blob("smoke_artifacts.zip")
blob.download_to_filename("smoke_artifacts.zip")
unzip_path = ""
with zipfile.ZipFile("smoke_artifacts.zip", 'r') as zip_ref:
    zip_ref.extractall(unzip_path)
os.remove("smoke_artifacts.zip")