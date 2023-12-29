from pathlib import Path
import os

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")


key_file_path = "key_service_account.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path
