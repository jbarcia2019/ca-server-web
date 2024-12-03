FROM python:3.11-slim

# Instalar dependencias
RUN apt-get update && apt-get install -y openssl && apt-get clean

# Crear estructura de directorios
WORKDIR /app
RUN mkdir -p /app/ca /app/certs

# Instalar Flask
RUN pip install flask

# Copiar los archivos del servidor
COPY app /app

# Exponer el puerto 5000
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "server.py"]
