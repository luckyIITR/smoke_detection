import os
import zipfile
from cnnClassifier import logger
from cnnClassifier.entity.config_entity import DataIngestionConfig
from cnnClassifier.utils.common import get_size
from google.cloud import storage
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        storage_client = storage.Client()

        bucket = storage_client.bucket(self.config.bucket_name)
        blob = bucket.blob(self.config.source_blob_name)

        if not os.path.exists(self.config.local_data_file):
            blob.download_to_filename(self.config.local_data_file)
            logger.info(f"Blob {self.config.source_blob_name} downloaded to {self.config.local_data_file}.")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
