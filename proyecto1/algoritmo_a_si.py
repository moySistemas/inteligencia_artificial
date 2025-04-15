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
#El 3 es inicio y el 4 fin
inicio = (2,3)
meta = (7,8)
mapa[inicio] = 3
mapa[meta] = 4

# Movimientos posibles: (fila, columna)
#Los moviemientos son: Derecha, abajo, izquierda, arriba
movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]  



#Función heurística - Distancia de Manhattan
def heuristica(nodo_actual, nodo_destino):
    return abs(nodo_actual[0] - nodo_destino[0]) + abs(nodo_actual[1] - nodo_destino[1])




print(heuristica(inicio,meta))