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
import cv2



from app.models.cancer_classifier import CancerClassifier  # Importa la clase del modelo
from models.images import ImageRequest
from utils.imagenes import decode_base64_image, make_gradcam_heatmap, overlay_heatmap



# Inicializa el clasificador
classifier = CancerClassifier("cancer_model.h5")

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

# ===============================
# Endpoint para recibir la imagen y devolver el resultado
# ===============================
@app.post("/predict/")
async def predict(image_request: ImageRequest):
    try:
        image = decode_base64_image(image_request.image_base64)
        # Procesar imagen
        imagen_procesada = classifier.preprocess_image(image_request.image_base64)
        
        # Hacer la predicción
        confianza, etiqueta = CancerClassifier.predict(imagen_procesada)

        # Aplicar Grad-CAM
        last_conv_layer_name = "conv5_block16_concat"  
        heatmap = make_gradcam_heatmap(imagen_procesada, CancerClassifier, last_conv_layer_name)
        gradcam_result = overlay_heatmap(image, heatmap)

        # Convertir imagen con Grad-CAM a Base64 para devolverla en la respuesta
        _, buffer = cv2.imencode(".png", gradcam_result)
        gradcam_base64 = base64.b64encode(buffer).decode("utf-8")

        return {
            "prediccion": etiqueta,
            "confianza": f"{confianza:.4f}",
            "imagen_gradcam": gradcam_base64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
