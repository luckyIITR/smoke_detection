from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    bucket_name: str
    source_blob_name: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float


@dataclass(frozen=True)
class CallbacksConfig:
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path

    batch_size: int  # set batch size for training
    epochs: int  # number of all epochs in training
    patience: int  # number of epochs to wait to adjust lr if monitored value does not improve
    stop_patience: int  # number of epochs to wait before stopping training if monitored value does not improve
    threshold: float  # if train accuracy is < threshold adjust monitor accuracy, else monitor validation loss
    factor: float  # factor to reduce lr by
    ask_epoch: int