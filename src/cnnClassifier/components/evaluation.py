import os
import tensorflow as tf
import pandas as pd
from cnnClassifier.entity.config_entity import EvaluationConfig
from pathlib import Path
from cnnClassifier.utils.common import save_json


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.test_gen = None

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

    def _test_gen(self):
        test_images = self.extract_from_path(self.config.test_path)
        test_images_df = self.createDataFrame(test_images)
        self.test_gen = self.loadDataset(test_images_df)
        return self.test_gen

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)

    def evaluation(self):
        model = self.load_model(self.config.model_path)
        self._test_gen()
        self.score = model.evaluate(self.test_gen)

    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)
