# Usar Alpine Linux como base
FROM python:3.9-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y luego instalar las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto en el que la aplicación estará escuchando
EXPOSE 5000

# Definir la variable de entorno para el puerto
ENV FLASK_RUN_PORT=5000

# Configurar Gunicorn para ejecutar la aplicación
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
