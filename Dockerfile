# Usa imagen base oficial de Python
FROM python:3.11-slim

# Establece directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .
COPY main.py .
COPY robertuito-reentrenado-v2/ ./robertuito-reentrenado-v2

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto por defecto de Uvicorn
EXPOSE 8080

# Comando para correr la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
