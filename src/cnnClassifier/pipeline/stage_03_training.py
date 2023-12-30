from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.callbacks import PrepareCallback
from cnnClassifier.components.training import Training
from cnnClassifier import logger

STAGE_NAME = "Training"


class ModelTrainingPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        config = ConfigurationManager()
        training_config = config.get_training_config()
        training = Training(config=training_config)
        training.get_base_model()
        train_df, valid_df, test_df = training.get_train_test_valid_df()
        training.get_data_generator(train_df, valid_df, test_df)

        training.get_augmentated_df(train_df)

        callbacks_config = config.get_callback_config()
        prepare_callbacks = PrepareCallback(config=callbacks_config)
        callback_list = prepare_callbacks.get_tb_ckpt_callbacks()

        training.train(
            callback_list=callback_list
        )


if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e