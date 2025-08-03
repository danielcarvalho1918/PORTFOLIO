# script que treina e salva o modelo

# train_model.py
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Carrega o dataset Iris
iris = load_iris()
X, y = iris.data, iris.target

# Cria e treina o modelo
model = RandomForestClassifier()
model.fit(X, y)

# Salva o modelo treinado
joblib.dump(model, 'model.joblib')

print("Modelo salvo como 'model.joblib'")
