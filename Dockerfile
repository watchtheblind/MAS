# 1. Imagen base de Python
FROM python:3.11-slim

# 2. Evita que Python genere archivos .pyc y permite que los logs salgan directo a la consola
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /code

# 4. Instalar dependencias del sistema (necesarias para psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalar dependencias de Python
COPY backend/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
# 6. Copiar el código del proyecto
COPY . /code/
# 7. Exponer el puerto de Django
EXPOSE 8000

# 8. Comando para arrancar la app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]