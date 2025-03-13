# Usa una imagen oficial de Python como imagen base
FROM python:3.11
# Establece el directorio de trabajo en el contenedor
WORKDIR /app
# Copia el contenido del directorio actual en el contenedor en /app
COPY ./app /app
# Instala los paquetes necesarios especificados en requirements.txt
RUN pip install -r requirements.txt
# Ejecuta main.py cuando se inicie el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]