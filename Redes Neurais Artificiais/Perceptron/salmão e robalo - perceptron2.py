# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 20:41:23 2025

@author: Daniel Carvalho Anselmo
"""


import pandas as pd

peixes = pd.read_csv('robalo-salmao.csv')


entrada1 = peixes['lightness'].tolist()
entrada2 = peixes['width'].tolist()

entrada = [[x, y] for x, y in zip(entrada1, entrada2)]
saida = peixes['species'].tolist()

X = entrada
y = saida


import math

# Função de ativação (sigmoide)
def sigmoide(x):
    return 1 / (1 + math.exp(-x))

# Derivada da sigmoide
def derivada_sigmoide(x):
    return x * (1 - x)

# Perceptron
class Perceptron:
    def __init__(self, input_size, taxa_aprendizado=0.1):
        self.taxa_aprendizado = taxa_aprendizado
        # Inicializando os pesos aleatoriamente
        self.pesos = [random.uniform(-1, 1) for _ in range(input_size)]
        # Inicializando o bias aleatoriamente
        self.bias = random.uniform(-1, 1)

    # Função para treinar o modelo
    def treinar(self, X, y, epocas):
        for _ in range(epocas):
            for i in range(len(X)):
                # Passo 1: cálculo da saída (com a fórmula de ativação)
                entrada = X[i]
                soma = sum(entrada[j] * self.pesos[j] for j in range(len(entrada))) + self.bias
                previsao = sigmoide(soma)
                
                # Passo 2: cálculo do erro
                erro = y[i] - previsao
                
                
                # Passo 3: ajuste dos pesos
                for j in range(len(self.pesos)):
                    self.pesos[j] += self.taxa_aprendizado * erro * derivada_sigmoide(previsao) * entrada[j]
                
                # Ajuste do bias
                self.bias += self.taxa_aprendizado * erro * derivada_sigmoide(previsao)
    
            print(f'Erro: {erro}')
    
    # Função para fazer previsões
    def prever(self, X):
        previsoes = []
        for entrada in X:
            soma = sum(entrada[j] * self.pesos[j] for j in range(len(entrada))) + self.bias
            previsao = sigmoide(soma)
            previsoes.append(1 if previsao >= 0.5 else 0)  # Limite de 0.5 para classificação binária
        return previsoes

# Importando o módulo random
import random

# Dados de entrada (camada de entrada)
"""X = [
    [2.834754, 21.087143],
    [3.329180, 18.877143],
    [3.690492, 19.824286],
    [4.812459, 17.760000],
    [4.812459, 16.497143],
    [4.926557, 16.181429],
    [1.256393, 15.550000],
    [1.636721, 20.140000],
    [1.998033, 19.970000],
    [2.872787, 18.245714]
]"""
    



# Rótulos das classes de saída (0 ou 1)
#y = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]


# Inicializando o perceptron com 2 entradas (lightness e width)
perceptron = Perceptron(input_size=2, taxa_aprendizado=0.1)

# Treinando o perceptron
perceptron.treinar(X, y, epocas=10000)

# Fazendo previsões
previsao = perceptron.prever(X)

# Exibindo os resultados
print("Previsões:", previsao)


def acuracia(y_real, y_predito):
    # Inicializando os valores de TP, FP, TN, FN
    TP = FP = TN = FN = 0
    
    # Percorrendo as listas de valores reais e previstos
    for real, predito in zip(y_real, y_predito):
        if real == 1 and predito == 1:
            TP += 1  # True Positive
        elif real == 0 and predito == 1:
            FP += 1  # False Positive
        elif real == 0 and predito == 0:
            TN += 1  # True Negative
        elif real == 1 and predito == 0:
            FN += 1  # False Negative
    
    # Calculando a acurácia
    acuracia = (TP + TN) / (TP + TN + FP + FN)
    return acuracia

# Fazendo previsões com o modelo
previsao = perceptron.prever(X)

# Calculando a acurácia
acuracia_resultado = acuracia(y, previsao)

# Exibindo a acurácia
print(f"Acurácia: {acuracia_resultado:.4f}")


def matriz_de_confusao(y_real, y_predito):
    # Inicializando os valores de TP, FP, TN, FN
    TP = FP = TN = FN = 0
    
    # Percorrendo as listas de valores reais e previstos
    for real, predito in zip(y_real, y_predito):
        if real == 1 and predito == 1:
            TP += 1  # True Positive
        elif real == 0 and predito == 1:
            FP += 1  # False Positive
        elif real == 0 and predito == 0:
            TN += 1  # True Negative
        elif real == 1 and predito == 0:
            FN += 1  # False Negative
    
    # Retorna a matriz de confusão
    return [[TP, FP], [FN, TN]]

# Fazendo previsões com o modelo
previsao = perceptron.prever(X)

# Calculando a matriz de confusão
confusao = matriz_de_confusao(y, previsao)

# Exibindo a matriz de confusão
print("Matriz de Confusão:")
for linha in confusao:
    print(linha)


