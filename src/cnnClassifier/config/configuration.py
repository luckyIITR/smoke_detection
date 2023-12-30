from cnnClassifier.constants import *
from cnnClassifier.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, CallbacksConfig, \
    TrainingConfig, EvaluationConfig
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

        callback_config = CallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)
        )

        return callback_config

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        params = self.params

        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "Chicken-fecal-images")
        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            base_model_path=Path(training.base_model_path),
            train_path=Path(training.train_path),
            test_path=Path(training.test_path),
            valid_path=Path(training.valid_path),
            img_size=params.IMAGE_SIZE,
            epochs=params.epochs,
            batch_size=params.batch_size,
            learning_rate=params.LEARNING_RATE
        )

        return training_config

    def get_validation_config(self) -> EvaluationConfig:
        config = self.config.evaluation
        eval_config = EvaluationConfig(
            model_path=config.model_path,
            test_path=config.test_path,
            img_size=self.params.IMAGE_SIZE,
            epochs=self.params.epochs,
            batch_size = self.params.BATCH_SIZE,
            learning_rate=self.params.LEARNING_RATE
        )
        return eval_config
