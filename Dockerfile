# syntax=docker/dockerfile:1.2
FROM python:latest

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y el código de la aplicación
COPY requirements.txt .
COPY api.py .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]