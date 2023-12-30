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


@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path  # to store the trained model
    base_model_path: Path  # load the base model

    train_path: Path
    test_path: Path
    valid_path: Path

    img_size: list
    epochs: int
    batch_size: int
    learning_rate: float


@dataclass(frozen=True)
class EvaluationConfig:
    model_path: Path
    test_path: Path

    img_size: list
    epochs: int
    batch_size: int
    learning_rate: float
