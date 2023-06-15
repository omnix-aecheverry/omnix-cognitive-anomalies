# Establecemos la imagen base en la que se construirá nuestra imagen, en este caso, una imagen de Python 3.9
FROM python:3.10.8-slim-buster

# Creamos un directorio para nuestra aplicación y establecemos ese directorio como el directorio de trabajo
WORKDIR /app

# Copiamos el archivo requirements.txt a ese directorio
COPY requirements.txt /app

# Instalamos los paquetes necesarios para nuestra aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos nuestro código fuente a ese directorio
COPY . /app

# Exponemos el puerto 3000 para que podamos acceder a nuestra API
EXPOSE 3000

# Especificamos el comando que se ejecutará cuando se inicie la imagen de Docker
CMD ["python", "main.py"]