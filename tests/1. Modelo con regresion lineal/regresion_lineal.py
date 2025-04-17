"""
Importamos pandas y ponemos pd como alias
Pandas permite leer archivos para despues hacer
analizarlos 
"""
import pandas as pd

"""
Para creacion de la grafica usa seaborn
"""
import seaborn as sb

"""
Matplolib me ayuda a mostrar el grafico si
no se trabaja en un entorno como google colab
"""
import matplotlib.pyplot as plt


"""
Crear el modelo usando sklearn con el modelo
LinearRegression
"""

from sklearn.linear_model import LinearRegression


#Leer el archivo csv
datos = pd.read_csv("celsius.csv")

#Imprimir informacion sobre el conjunto de datos
#datos.info()

#Un vistazo de los registros
#print(datos.head())


#Creando una grafica con seaborn
#sb.scatterplot(x="celsius",y="fahrenheit",data=datos)
#plt.show()


#1. Preparamos los datos
"""
Se separan en las caracteristicas
Caracteristicas (X) X mayuscula y la etiqueta (y) con y Minusucla
Caracteristica (X),(y)
X son los datos de entrada (grados cel)
y nuestra etiqueta o respuesta es y (grados fah)
"""

X = datos["celsius"]
y = datos["fahrenheit"]

#Transformar el arreglo x 
"""
Esta tranformacion se hace porque 
los datos que tenemos tienen el formato
array[40,20,10] y necesitamos [[40],[20,10]]
ya que existen problemas que tendran mas de una
caracteristica y una sola etiqueta o salida
"""
X_procesada = X.values.reshape(-1,1)
y_procesada = y.values.reshape(-1,1)


#2. Crear el modelo y entrenar el modelo

#Creamos el modelo
modelo = LinearRegression()

#Entrenamos el modelo con nuestros X e Y
modelo.fit(X_procesada,y_procesada)

#Pedimos una prediccion
print(modelo.predict([[123]]))

#Podemos ver que tan bien quedo entrenado el modelo segun lso datos
print(modelo.score(X_procesada, y_procesada)) #1 es el maximo nivel 





