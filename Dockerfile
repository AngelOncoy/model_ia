# Usa imagen base oficial de Python
FROM python:3.11-slim

# Establece directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el código
COPY requirements.txt .
COPY main.py .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instala gsutil (Google Cloud SDK básico)
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && apt-get install -y google-cloud-sdk

# Descarga el modelo desde GCS
RUN mkdir Robertuito-reentrenado-v2 && \
    gsutil -m cp -r gs://modelo-depresion-v1/Robertuito-reentrenado-v2/* ./Robertuito-reentrenado-v2/

# Expone el puerto
EXPOSE 8080

# Comando para ejecutar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
