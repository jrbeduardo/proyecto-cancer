import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

class MalariaClassifier:
    def __init__(self, model_path: str):
        """
        Inicializa el clasificador cargando el modelo.

        :param model_path: Ruta del archivo del modelo (.h5).
        """
        self.model = tf.keras.models.load_model(model_path, compile=False)

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocesa una imagen para hacerla compatible con el modelo.

        :param image: Imagen en formato PIL.
        :return: Imagen preprocesada como un array de NumPy.
        """
        image = image.resize((224, 224))  # Redimensionar la imagen
        image = img_to_array(image) / 255.0  # Normalizar los píxeles
        return np.expand_dims(image, axis=0)  # Añadir dimensión para batch

    def predict(self, img_array: np.ndarray) -> dict:
        """
        Realiza una predicción en la imagen preprocesada.

        :param img_array: Imagen preprocesada como un array de NumPy.
        :return: Diccionario con el resultado de la predicción.
        """
        predictions = self.model.predict(img_array).tolist()[0]
        confidence = max(predictions)
        predicted_class = np.argmax(predictions)
        return {
            "confidence": round(confidence, 2),
            "malaria": confidence,
            "predicted_class": "Sí malaria" if predicted_class == 1 else "No malaria"
        }
