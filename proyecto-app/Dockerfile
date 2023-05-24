# Utiliza la imagen base de Python 3.9 slim
FROM python:3.9-slim-bullseye

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY ./app /app

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 80 para acceder a la aplicación
EXPOSE 80

# Ejecuta la aplicación con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
