from fastapi import FastAPI,UploadFile, File, Query, HTTPException
from models.images import ImageData

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

from fastapi.middleware.cors import CORSMiddleware

###### CARGA DE MODELO

model = tf.keras.models.load_model(
    'malaria_detection_model.h5', 
    compile = False
)

app = FastAPI()

@app.post("/clasification_image", tags=["Clasificador de malaria"])
def upload_image(image_data: ImageData):
    try:
        # Decodificar la imagen base64
        image_data_bytes = base64.b64decode(image_data.img_base64)
        image = Image.open(BytesIO(image_data_bytes))
        # Preprocesar la imagen para el modelo
        image = image.resize((224,224))
        image = img_to_array(image) / 255.0
        img_array = np.expand_dims(image, axis=0)

        # Realizar la predicción
        data = {}
        confidence = max(model.predict(img_array).tolist()[0])
        data["prediction"] = round(confidence,2)
        data['malaria'] = True if confidence >= 0.95 else False
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the image: {str(e)}")