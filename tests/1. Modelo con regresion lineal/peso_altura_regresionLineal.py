import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


"""
Caracteristica: X,y
X (entrada) = altura
y(etiqueta,salida) = peso

"""

#Utiliza pandas para leer el archivo csb
datos = pd.read_csv("peso_altura.csv")

#Creando una grafica con seaborn e imprime con matplolib
#sb.scatterplot(x="Altura (m)", y="Peso (kg)", data=datos)
#plt.show()

#1. Preparacion de los datos
X = datos["Altura (m)"]
y =datos["Peso (kg)"]

#Transformar de serie a dataframe para poder tener varios datos de entrada
X_procesada = X.values.reshape(-1,1)
y_procesada = y.values.reshape(-1,1)


#2. Crear el modelo y entrenar el modelo

#Crear el modelo
modelo = LinearRegression()

#Entrenar el modelo
modelo.fit(X_procesada,y_procesada)

#Pedimos una prediccion
print(modelo.predict([[1.7]]))


#Ver que tan preciso quedo el modelo
print(modelo.score(X_procesada, y_procesada))






