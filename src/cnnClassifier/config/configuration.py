from cnnClassifier.constants import *
from cnnClassifier.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, CallbacksConfig
from cnnClassifier.utils.common import read_yaml, create_directories


class ConfigurationManager:
    """
        responsible for creating the Directories needed for data
        and return entity -> DataIngestionConfig
    """

    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            bucket_name=config.bucket_name,
            source_blob_name=config.source_blob_name,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model

        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
        )

        return prepare_base_model_config

    def get_callback_config(self) -> CallbacksConfig:
        config = self.config.callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_directories([
            Path(model_ckpt_dir),
            Path(config.tensorboard_root_log_dir)
        ])
        param_config = self.params

        callback_config = CallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath),
            batch_size=param_config.batch_size,  # set batch size for training
            epochs=param_config.epochs,  # number of all epochs in training
            patience=param_config.patience,  # number of epochs to wait to adjust lr if monitored value does not improve
            stop_patience=param_config.stop_patience,
            # number of epochs to wait before stopping training if monitored value does not improve
            threshold=param_config.threshold,
            # if train accuracy is < threshold adjust monitor accuracy, else monitor validation loss
            factor=param_config.factor,  # factor to reduce lr by
            ask_epoch=param_config.ask_epoch,  # number of epochs to run before asking if you want to halt training
        )

        return callback_config
