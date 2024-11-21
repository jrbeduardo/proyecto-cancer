
# Documentación General de la API

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
   - [Clonación del Repositorio](#clonación-del-repositorio)
   - [Configuración del Entorno](#configuración-del-entorno)
4. [Uso de Docker](#uso-de-docker)
   - [Construcción de la Imagen](#construcción-de-la-imagen)
   - [Ejecución del Contenedor](#ejecución-del-contenedor)
   - [Detener y Eliminar Contenedores](#detener-y-eliminar-contenedores)
5. [Endpoints de la API](#endpoints-de-la-api)
   - [GET /endpoint1](#get-endpoint1)
   - [POST /endpoint2](#post-endpoint2)
   - [PUT /endpoint3](#put-endpoint3)
   - [DELETE /endpoint4](#delete-endpoint4)
6. [Manejo de Errores](#manejo-de-errores)
7. [Pruebas](#pruebas)

---

## Introducción
Esta documentación describe cómo configurar, ejecutar y usar una API mediante Docker. Proporciona detalles sobre los endpoints disponibles, la instalación, y cómo manejar errores y contribuciones.

## Requisitos Previos
- Docker y Docker Compose instalados.
- Git instalado.
- Configuración básica del sistema operativo.

## Instalación

### Clonación del Repositorio
Clona el repositorio del proyecto:
```bash
git clone https://github.com/usuario/proyecto-api.git
cd proyecto-api
```

### Configuración del Entorno
Crea un archivo `.env` basado en el archivo de ejemplo incluido:
```bash
cp .env.example .env
```
Edita las variables de entorno según sea necesario.

---

## Uso de Docker

### Construcción de la Imagen
Construye la imagen de Docker:
```bash
docker build -t nombre-imagen .
```

### Ejecución del Contenedor
Inicia el contenedor con Docker:
```bash
docker run -d -p 5000:5000  nombre-imagen
```
Accede a la API en `http://localhost:5000`.

### Detener y Eliminar Contenedores
Para detener un contenedor:
```bash
docker stop id_contenedor
```
Para eliminarlo:
```bash
docker rm id_contenedor
```

---

## Endpoints de la API

### GET /endpoint1
Descripción: Obtiene información.
```bash
curl -X GET http://localhost:5000/endpoint1
```

### POST /endpoint2
Descripción: Crea un recurso.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://localhost:5000/endpoint2
```

### PUT /endpoint3
Descripción: Actualiza un recurso.
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"key":"new_value"}' http://localhost:5000/endpoint3
```

### DELETE /endpoint4
Descripción: Elimina un recurso.
```bash
curl -X DELETE http://localhost:5000/endpoint4
```

---

## Manejo de Errores
La API devuelve respuestas HTTP con códigos de error estándar:
- **400**: Solicitud incorrecta.
- **404**: Recurso no encontrado.
- **500**: Error interno del servidor.

---

## Pruebas
Ejecuta las pruebas incluidas:
```bash
pytest tests/
```



