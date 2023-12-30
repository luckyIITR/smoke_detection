import os
import tensorflow as tf
import pandas as pd
from cnnClassifier.entity.config_entity import TrainingConfig
from pathlib import Path


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.model = None
        self.history = None
        self.train_gen = None
        self.valid_gen = None
        self.test_gen = None
        self.train_data_aug_20 = None

    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.base_model_path
        )
        return self.model

    @staticmethod
    def extract_from_path(path) -> []:
        full_path = []
        for i in sorted(os.listdir(path)):
            full_path.append(os.path.join(path, i))
        return full_path

    @staticmethod
    def createDataFrame(image_paths):
        labels = [path.split('/')[-1].split('_')[0] for path in image_paths]
        df = pd.DataFrame({'path': image_paths, 'label': labels})
        df['label_id'] = df['label'].apply(lambda x: 1 if x == 'smoking' else 0)
        return df

    def get_train_test_valid_df(self):
        train_images = self.extract_from_path(self.config.train_path)
        test_images = self.extract_from_path(self.config.test_path)
        valid_images = self.extract_from_path(self.config.valid_path)
        train_images_df = self.createDataFrame(train_images)
        test_images_df = self.createDataFrame(test_images)
        valid_images_df = self.createDataFrame(valid_images)

        return train_images_df, test_images_df, valid_images_df

    def imgPreProcessing(self, image, label):
        img = tf.io.read_file(image)
        img = tf.io.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, size=(self.config.img_size))
        return img, label

    def loadDataset(self, df: pd.DataFrame):
        dataset = tf.data.Dataset.from_tensor_slices((df['path'], df['label_id']))
        return (dataset
                .map(self.imgPreProcessing)
                .shuffle(self.config.batch_size * 20)
                .batch(self.config.batch_size))

    def get_data_generator(self, train_df, valid_df, test_df):
        train_gen = self.loadDataset(train_df)
        test_gen = self.loadDataset(test_df)
        valid_gen = self.loadDataset(valid_df)
        self.train_gen = train_gen
        self.test_gen = test_gen
        self.valid_gen = valid_gen

        return train_gen, test_gen, valid_gen

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    @staticmethod
    def augmentation(image, label):
        SEED = 42
        img = tf.image.random_flip_left_right(image, seed=SEED)
        img = tf.image.random_brightness(img, 0.1, seed=SEED)
        img = tf.image.random_contrast(img, 0.2, 0.5, seed=SEED)
        img = tf.image.random_saturation(img, .5, 1, seed=SEED)
        img = tf.image.random_hue(img, 0.2, seed=SEED)
        return img, label

    def loadDatasetWithAugmentaion(self, df: pd.DataFrame):
        dataset = tf.data.Dataset.from_tensor_slices((df['path'], df['label_id']))
        return (dataset
                .map(self.imgPreProcessing)
                .map(self.augmentation)
                .shuffle(self.config.batch_size * 20)
                .batch(self.config.batch_size)
                )

    def get_augmentated_df(self, train_df):
        # Loading only 25 % for data augmentaion
        data_size = len(train_df)
        self.train_data_aug_20 = self.loadDatasetWithAugmentaion(train_df.sample(frac=1)[:int(0.25 * data_size)])

    def train(self, callback_list: list):

        self.model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.Adam(),
                           metrics=["accuracy"])
        self.history = self.model.fit(
            self.train_data_aug_20, epochs=self.config.epochs,
            steps_per_epoch=len(self.train_data_aug_20),
            validation_data=self.valid_gen,
            validation_steps=len(self.valid_gen),
            callbacks=callback_list
        )
        # Fine tune the EfficientNetB0 layer
        print("Fine tune the EfficientNetB0 layer")
        base_eff_modelTwo_base = self.model.layers[1]
        base_eff_modelTwo_base.trainable = True
        # Freeze all layers except for the last 10
        for layer in base_eff_modelTwo_base.layers[:-10]:
            layer.trainable = False

        for no, layer in enumerate(base_eff_modelTwo_base.layers):
            print("Layer no : ", no, "Trainable : ", layer.trainable, "Layer Name : ", layer.name, )

        print("Total trainable parameters in the model ", len(self.model.trainable_variables))
        # Initila 2 + now unfreeing 10 = 12

        # recompiling the model
        self.model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                           optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate),
                           metrics=['accuracy'])
        fine_tune_epochs = self.config.epochs + 5
        self.history = self.model.fit(self.train_gen, epochs=fine_tune_epochs,
                                      steps_per_epoch=len(self.train_gen),
                                      initial_epoch=self.history.epoch[-1],
                                      validation_data=self.valid_gen,
                                      validation_steps=len(self.valid_gen),
                                      callbacks=callback_list
                                      )

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )