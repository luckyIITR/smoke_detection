from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
from cnnClassifier.config.configuration import ConfigurationManager
from io import BytesIO
import requests
from cnnClassifier.constants import CONFIG_FILE_PATH
from cnnClassifier.utils.common import read_yaml


class PredictionPipeline:
    def __init__(self):
        self.config = read_yaml(CONFIG_FILE_PATH)
        # load model
        self.model = load_model(self.config.training.trained_model_path)
        # self.params = read_yaml(PARAMS_FILE_PATH)

    @staticmethod
    def preprocess_image(image_bytes, img_shape=224):
        """Will take the image bytes and return the processed image"""
        image_data = BytesIO(image_bytes)
        image = Image.open(image_data)
        image = image.convert("RGB")
        image = image.resize((img_shape, img_shape))
        image_array = np.array(image)
        img = np.expand_dims(image_array, axis=0)
        return img

    @staticmethod
    def download_image(url):
        """ will return image binary data"""
        response = requests.get(url)
        image_bytes = response.content
        return image_bytes

    def predict(self, img):
        prediction = self.model.predict(img, verbose=0)
        # predicted_label = np.argmax(prediction)
        print(f"Smoking with probability {prediction[0][1] * 100}")
        print(f"Non-Smoking with probability {prediction[0][0] * 100}")

        return {"SmokingProbability": prediction[0][1] * 100,
                "NonSmokingProbability": prediction[0][0]*100}
