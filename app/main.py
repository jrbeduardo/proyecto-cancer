from fastapi import FastAPI,UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# Conversion Base64
import base64
from io import BytesIO

# TensorFlow
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array


import os
from PIL import Image, ImageOps
import io
import numpy as np



from models.malaria_classifier import MalariaClassifier  # Importa la clase del modelo
from models.images import ImageData


# Inicializa el clasificador
classifier = MalariaClassifier("malaria_detection_model.h5")

# Inicializa API
app = FastAPI()


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/clasification_image", tags=["Clasificador de malaria"])
def upload_image(image_data: ImageData):
    try:
        # Decodificar la imagen Base64
        image_data_bytes = base64.b64decode(image_data.img_base64)
        image = Image.open(BytesIO(image_data_bytes))
        
        # Preprocesar la imagen
        img_array = classifier.preprocess_image(image)
        
        # Realizar predicción
        result = classifier.predict(img_array)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the image: {str(e)}")
