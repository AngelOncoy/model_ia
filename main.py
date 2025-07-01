from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Cargar modelo y tokenizer desde carpeta local
model = AutoModelForSequenceClassification.from_pretrained("./Robertuito-reentrenado-v2", use_safetensors=True)
tokenizer = AutoTokenizer.from_pretrained("./Robertuito-reentrenado-v2")
model.eval()

# Diccionario de etiquetas
id2label = {0: "normal", 1: "ansiedad", 2: "depresivo"}

# Inicializar API
app = FastAPI()

# Entrada esperada
class TextoEntrada(BaseModel):
    texto: str

# Endpoint
@app.post("/analizar")
def analizar_texto(data: TextoEntrada):
    inputs = tokenizer([data.texto], return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1).squeeze().tolist()

    resultado = {id2label[i]: round(prob * 100, 2) for i, prob in enumerate(probs)}
    return {"resultado": resultado}
