import tkinter as tk
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Cargar modelo y tokenizer
model = AutoModelForSequenceClassification.from_pretrained("robertuito-reentrenado-v2", use_safetensors=True)
tokenizer = AutoTokenizer.from_pretrained("robertuito-reentrenado-v2")
model.eval()

# Crear ventana
ventana = tk.Tk()
ventana.title("Detector de Ansiedad y Depresión")

entrada_texto = tk.Text(ventana, height=5, width=50)
entrada_texto.pack()

resultado_label = tk.Label(ventana, text="")
resultado_label.pack()

id2label = {0: "Normal", 1: "Ansiedad", 2: "Depresivo"}

def analizar():
    texto = entrada_texto.get("1.0", tk.END).strip()
    inputs = tokenizer([texto], return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1).squeeze()
    resultados = "".join([f"{id2label[i]}: {probs[i]*100:.2f}%\n" for i in range(len(probs))])
    resultado_label.config(text=resultados)

boton = tk.Button(ventana, text="Analizar", command=analizar)
boton.pack()

ventana.mainloop()