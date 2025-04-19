#Regresion logistica

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split #Para serparar las X e y en entrenamiento y pruebas
from sklearn.linear_model import LogisticRegression #Importamos regresion logistica para crear el modelo
from sklearn.metrics import accuracy_score #Se usa para saber metricas de nuestro modelo como la exactitud
from sklearn.metrics import classification_report #Mas metricas
from sklearn.metrics import confusion_matrix #Para crear la matriz de confuncion


#Leer los datos del archivo
datos = pd.read_csv("titanic.csv")


#1.-------LIMPIAR EL DATA SET---------------------

#Ver los datos en el dataset
print(datos.head())

#Describir los datos
print(datos.describe())

#Creando una grafica con las personas que sobrevivieron
#sb.countplot(x="Survived", data=datos)
#Modificando la grafica para que nos diga si los sobrevientes eran hombres o mujeres
sb.countplot(x="Survived",data=datos,hue="Sex")
plt.show()


#Para ver los datos vacios que tenemos por columna
print(datos.isna().sum()) #Hay datos que estan vacios tenemos que ver que hacer con eos

#Hacemos una grafica para ver la distribucion de las edades 
sb.displot(x="Age", data=datos)
plt.show() 

#Notamos que las edades comunes son entre 15-35 anios
#Para ver una tabla con las edades podemos
print(datos["Age"])
#Para saber el promedio de edades
print(datos["Age"].mean())
#Para rellenar datos vacios con el promedio
#Asi como existe dropna para borrar existe fillna
#print(datos["Age"].fillna(datos["Age"].mean()))
#La modiciacion hay que agregarselo al set de datos
datos["Age"] = datos["Age"].fillna(datos["Age"].mean())
#Si volvemos a imprimir la cantidad de datos vacios veremos que edad no tiene registros vacios
print(datos.isna().sum())

#Ahora la cabina tambien tiene datos vacios. Vamos a eliminarlo
#Pusimos el axis para especificar que es una columna
datos = datos.drop(["Cabin"], axis=1)
#Volvemos a imprimir los datos vacios
print(datos.isna().sum())


#Ahora los datos de embarcacion
#Simplemente eliminamos los dos datos vacios
#Deveriamos especificar una columna pero como no hay mas datos vacios
#Es seguro ejecutalo de esa forma
datos = datos.dropna()
#Volmemos a ver los datos vacios
print(datos.isna().sum())



#Volvemos a ver nuestro setdatos
print(datos.head())
#Vamos a eliminar las siguientes columnas: 
datos = datos.drop(["Name", "PassengerId", "Ticket"], axis=1)
print(datos.head())


#Ahora debemos de convertir el dato sexo en numerico
#Lo podemos hacer con pd.get_dummies(datos["Sex"]) y nos devuelve
#dos columnas una con female y otra con male 
#print(pd.get_dummies(datos["Sex"]).astype(int))

#Siempre que female es 0 male es 1, entonces tenemos datos redundantes
#Podemos eliminar una de las columnas para solo tener si es hombre o no
dummies_sex = (pd.get_dummies(datos["Sex"], drop_first=True).astype(int))
#Unimos la nueva tabla a las caracteristicas
datos = datos.join(dummies_sex)
#Borramos la columna de sexo con drop
datos = datos.drop(["Sex"], axis=1)
#Volvemos a ver los datos
print(datos.head())


#Embarcado
#Hacemos una grafica para saber si es relevante
sb.countplot(x="Survived", data=datos, hue="Embarked")
plt.show()

#Como no queda tan claro con la grafica vamos a hacer dummies
#A continuacion se dejan solo dos columnas para embarked con 1 y 0
#Se unen las columnas a las caracteristicas
#Se borra embarked
#Se muestran los nuevos datos
dummies_embarked = pd.get_dummies(datos["Embarked"], drop_first=True).astype(int)
datos = datos.join(dummies_embarked)
datos = datos.drop(["Embarked"], axis=1)
print(datos.head())






#2. ------------ CORRELACION DE DATOS ----------

#Creamos una grafica de correlacion y nuestro caso es ver 
#Quienes sobrevivieron
sb.heatmap(datos.corr(), annot=True, cmap="YlGnBu")
plt.show()

#Creamos otra grafica para que quede mas claro
sb.countplot(x="Survived", data=datos, hue="Pclass")
plt.show()








#3. -------------------- ENTRENAMIENTO -------------


#Separamos las X y y

X = datos.drop(["Survived"], axis=1)
y = datos["Survived"]



#Separar las X e y entrenamiento y pruebas
X_ent, X_pru, y_ent, y_pru = train_test_split(X,y, test_size=.2)



#Creamos el modelo


#Lo que se pone entre parentesis es cuantas veces va a iterar para intentar ajustar la funcion
modelo =LogisticRegression(max_iter=1000)
modelo.fit(X_ent, y_ent)



#4 -------------------- PRUEBAS -----------------------

predicciones = modelo.predict(X_pru)

#Exactitud del modelo
print(accuracy_score(y_pru, predicciones))

#Otros datos de metrica
print(classification_report(y_pru, predicciones))

#Matriz de confucion
#Creamos un dataframe de pandas
print(pd.DataFrame(confusion_matrix(y_pru, predicciones), columns=["Pred: No", "Pred:Si"], index=["Real:No", "Real:Si"]))



#5------------------Agregando una nueva persona al modelo y probar resultado

nueva_persona = [1,35,0,0,80,1,0,0] #Los numeros salen de las columnas

prediccion = modelo.predict([nueva_persona])

if prediccion[0] == 1:
	print("Sobrevisite")

else:
	print("No Sobrevisite")