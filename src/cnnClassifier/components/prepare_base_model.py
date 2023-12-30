from cnnClassifier.entity.config_entity import PrepareBaseModelConfig
import tensorflow as tf
from pathlib import Path
from cnnClassifier import logger


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.full_model = None
        self.model = None
        self.config = config

    def get_base_model(self):
        self.model = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False)
        self.save_model(path=self.config.base_model_path, model=self.model)

    @staticmethod
    def _prepare_full_model(model, learning_rate, IMAGE_SIZE):
        model.trainable = False

        input_ = tf.keras.layers.Input(shape=tuple(IMAGE_SIZE) + (3,), name="input layer")
        x = model(input_)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)

        output = tf.keras.layers.Dense(2, activation="sigmoid")(x)

        base_model = tf.keras.Model(input_, output)
        base_model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                           optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), metrics=["accuracy"])
        base_model.summary()
        return base_model

    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            learning_rate=self.config.params_learning_rate,
            IMAGE_SIZE=self.config.params_image_size
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
