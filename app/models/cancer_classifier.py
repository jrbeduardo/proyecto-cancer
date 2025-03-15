import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
from utils.modelo_cancer import create_model
from utils.imagenes import decode_base64_image, preprocess_image

class CancerClassifier:
    def __init__(self, model_path: str):
        """
        Inicializa el clasificador cargando el modelo.

        :param model_path: Ruta del archivo del modelo (.h5).
        """
        self.model = create_model()

        # Cargar solo los pesos
        self.model.load_weights(self.model)

        # Compilar el modelo
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
        self.model.compile(optimizer=optimizer,
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])


    def preprocess_image(self, image_base64: str):
        """
        Preprocesa una imagen para hacerla compatible con el modelo.

        :param image: Imagen en formato PIL.
        :return: Imagen preprocesada como un array de NumPy.
        """
        # Convertir imagen Base64 a NumPy array
        image = decode_base64_image(image_base64)

        # Preprocesar imagen
        imagen_procesada = preprocess_image(image)
        return imagen_procesada

    def predict(self, img_array: np.ndarray):
        """
        Realiza una predicción en la imagen preprocesada.

        :param img_array: Imagen preprocesada como un array de NumPy.
        :return: Diccionario con el resultado de la predicción.
        """
        # Hacer la predicción
        y_pred_probs = self.model.predict(img_array)
        clase_predicha = tf.argmax(y_pred_probs, axis=1).numpy()[0]  # Obtener la clase con mayor probabilidad
        confianza = np.max(y_pred_probs)
        etiqueta = "Maligno" if clase_predicha == 1 else "Benigno"

        return confianza, etiqueta
