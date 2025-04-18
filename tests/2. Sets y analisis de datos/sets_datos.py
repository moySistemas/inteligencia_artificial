import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


#Lectura del data set con pandas
datos = pd.read_csv("casas.csv")

#Ver los primeros 5 datos del set
print(datos.head())


'''
La columna ocean_proxi no es un dato
numerico y deberos hacer tranformaciones
'''

#Para ver lo que hay en la columa ocean_proximity
print(datos["ocean_proximity"])
#Para ver cuantos datos disntitos hay en ocen_proximity
print(datos["ocean_proximity"].value_counts())


#Para ver cuantos datos vienen no vacio y tipo dato
print(datos.info())

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
datos.hist(figsize=(15,8), bins=30, edgecolor="black")
#hacemos que la grafica se muestre usando matplolib
plt.show()


#Creando una mejor grafica con seaborn
sb.scatterplot(
    x="latitude",
    y="longitude",
    data=datos,
    hue="median_house_value",
    palette="coolwarm",
    size="population",              
    sizes=(10, 200),                
    legend=False                    
)
plt.show()



#-----Mejorando el set---------

#1. Tratamiento a las celdas vacias
'''
En el dataset hay datos vacios, entonces para este ejemplo
es mejor quitarlos
'''

#Quitando los datos vacios
datos_na = datos.dropna()
print("Datos sin datos vacios")
print(datos_na.info())


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
print(datos_na.head())


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
sb.set(rc={'figure.figsize':(8,8)})
sb.heatmap(datos_na.corr(), annot=True, cmap="YlGnBu")
plt.show()

#El precio de la casa se relaciona con la media de ingresos
#Correlacion concentrados solo en el precio de la casa
print(datos_na.corr()["median_house_value"].sort_values(ascending=False))