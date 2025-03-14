import numpy as np
"""
Se usa el 0 para los espacios vacios
y el 1 para los espacios con obstaculo.
"""


#Definicion del mapa (con todo en ceros)
mapa = np.zeros((10,10),dtype=int)



#El formato es: fila, columna
#En la fila 3 y en la columna del 3 a 6 se asigna un 1 (obstaculo)
#En la fila 6 y en la columna del 2 a 7 se asigna un 1 (obstaculo)
mapa[3, 3:7] = 1 
mapa[6, 2:8] = 1


#Inicio(punto de partida), meta(punto final)
#tupla(fila,columna)
inicio = (7,0)
meta = (9,9)
mapa[inicio] = 3
mapa[meta] = 4


print(mapa)

