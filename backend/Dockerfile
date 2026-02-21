# Imagen base de Python ligera
FROM python:3.12-slim

# Evitar que Python genere archivos .pyc y forzar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias de sistema necesarias para PyMuPDF (fitz)
RUN apt-get update && apt-get install -y \
    build-essential \
    libmupdf-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear la carpeta de almacenamiento para los PDFs
RUN mkdir -p storage

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para arrancar uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]