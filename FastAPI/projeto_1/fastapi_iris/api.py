# API FastAPI que carrega e serve o modelo

# api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Inicia a aplicação FastAPI
app = FastAPI()

# Carrega o modelo treinado
model = joblib.load("model.joblib")

# Define o formato da entrada da API
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Endpoint de predição
@app.post("/predict")
def predict(data: IrisInput):
    # Prepara os dados para o modelo
    input_data = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])

    # Faz a predição
    prediction = model.predict(input_data)
    predicted_class = int(prediction[0])

    return {"predicted_class": predicted_class}
