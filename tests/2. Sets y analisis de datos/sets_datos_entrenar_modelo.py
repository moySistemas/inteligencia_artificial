import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split #Libreria para poder dividir el dataset en dos
from sklearn.linear_model import LinearRegression #Libreria para poder entrenar el modelo
from sklearn.metrics import mean_squared_error #Para calcular el error en nuestor modelo
import numpy as np
from sklearn.preprocessing import StandardScaler


#Lectura del data set con pandas
datos = pd.read_csv("casas.csv")

#Ver los primeros 5 datos del set
#print(datos.head())


'''
La columna ocean_proxi no es un dato
numerico y deberos hacer tranformaciones
'''

#Para ver lo que hay en la columa ocean_proximity
#print(datos["ocean_proximity"])
#Para ver cuantos datos disntitos hay en ocen_proximity
#print(datos["ocean_proximity"].value_counts())


#Para ver cuantos datos vienen no vacio y tipo dato
#print(datos.info())

'''
En primer lugar, los algoritmos de IA necesitan
que todos los datos sean numericos y ocean_proximity es
de tipo caracter. Y en segundo lugar, total_bedrooms le faltan
200 datos. Podemos rellenar los datos con los valores o eliminar esos 
datos.
'''

#Por cada columna da diferentes datos
print(datos.describe())

#Usamos la funcion hist para hacer histogramas
#datos.hist(figsize=(15,8), bins=30, edgecolor="black")
#hacemos que la grafica se muestre usando matplolib
#plt.show()


#Creando una mejor grafica con seaborn
#sb.scatterplot(
#    x="latitude",
#    y="longitude",
#    data=datos,
#    hue="median_house_value",
#    palette="coolwarm",
#    size="population",              
#    sizes=(10, 200),                
#    legend=False                    
#)
#plt.show()



#-----Mejorando el set---------

#1. Tratamiento a las celdas vacias
'''
En el dataset hay datos vacios, entonces para este ejemplo
es mejor quitarlos
'''

#Quitando los datos vacios
datos_na = datos.dropna()
#print("Datos sin datos vacios")
#print(datos_na.info())


#2. Tramiento a las columnas con letras

'''
Convertir la caracteristica categorica a numerica
'''

#Usar dummies / One hot enconding
#Near bay inland near ocean, si la casa esta en inlad tendra 1,
#si esta en near bay entonces 1 y el resto 0

#Usar panda para aplicar dummis
dummies = pd.get_dummies(datos_na["ocean_proximity"], dtype=int)

#Agregar al final los dummies en el datos_na
datos_na = datos_na.join(dummies)
#Incluye dummies
#print(datos_na.head())


#Ahora debemos borrar la columna de ocean_proximity porque no tiene uso
#axis es columna, le decimos que ocean es una columna
datos_na = datos_na.drop(["ocean_proximity"],axis=1)


#3. Correlaciones

'''
se puede usar datos_na.corr() para 
obtener una correlacion. 
Lo importante en la correlacion es que variables
tienen impacto sobre otras. Podemos ignorar 
aquellas cercanas a 0
'''

#Para que no se vea en una tabla y mejor en grafica
#Un 1 es una relacion perfecta 
#sb.set(rc={'figure.figsize':(8,8)})
#sb.heatmap(datos_na.corr(), annot=True, cmap="YlGnBu")
#plt.show()

#El precio de la casa se relaciona con la media de ingresos
#Correlacion concentrados solo en el precio de la casa
print(datos_na.corr()["median_house_value"].sort_values(ascending=False))






#4. Entrenamiento del modelo

#Separar las caracteristicas de la etiqueta

'''
En X guardamos la caracteristica y necesitamos quitar
la columna de median_house_values.

En y vamos a guardar la etiqueta o resultado que para
este modelos sera median_model_value
'''

#Eliminamos median_house_value de las caracteristicas
X = datos_na.drop(["median_house_value"], axis=1)
#Definer en y media_house_value como etiqueta o salida
y = datos_na["median_house_value"]


#Separar los datos en 2 partes: Conjunto de entrenamiento y pruebas

    #Usando sklearn podemos separ el dataset en dos
X_ent, X_pru, y_ent, y_pru = train_test_split(X,y, test_size=.2) #Le decimos que de X y y tome el 20% para pruebas

#Imprimir (cantidad de datos, columnas)
#print(X_pru.shape)


#Creamos el modelo
modelo = LinearRegression()

#Entrenamos el modelo usando X y y de entrenamiento
modelo.fit(X_ent, y_ent)






#Hacer predicciones con el dataset de pruebas

predicciones = modelo.predict(X_pru)


#comparamos valores
#Se hace una tabla con los valores calculados de y en prediccion y se compara con el y real
comparativa = {"Prediccion": predicciones, "Valor Real":y_pru} 
print(pd.DataFrame(comparativa)) #Se crea una tabla con pandas




#6. Saber la precision del modelo

#El modelo funciona bien con los datos de entrenamiento pero mal con los de prueba
#A esto ultimo se le llama Overfitting sobreajuste

print(modelo.score(X_ent, y_ent))
print(modelo.score(X_pru, y_pru))



#Error
#Calcular que tanto se falla en las predicciones


mse = mean_squared_error(y_pru, predicciones)
rmse = np.sqrt(mse)
print("En promedio cuanto hemos fallado calculado el precio", rmse)


#Revisar el scaler o escalamiento

'''
Por la propia naturaleza de los datos algunos 
datos son muy pequenos y podemos ver esto con 
describe(), un modelo le dara mas peso a los numeros
grandes.
Con el scaler se comprimen los datos para que todos 
esten en el mismo rango y el modelo no le mas peso 
a un numero mas grande. Esto solo se hace en las caracteristicas X
y no en la y de salita o etiqueta
'''

#Escalar los datos de entrenamiento
scaler = StandardScaler()
X_ent_esc = scaler.fit_transform(X_ent)
X_pru_esc = scaler.fit_transform(X_pru)


#Aqui ya no tenemos numeros grandes
print(pd.DataFrame(X_ent_esc))
#Con esos datos se puede volver a entrenar el modelo
#Esperando tener mejores resultados



