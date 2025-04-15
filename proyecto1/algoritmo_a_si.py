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


def algoritmo_a_estrella(mapa, inicio, meta):
    lista_abierta = [inicio]  
    camino_desde = {}  
    costo_real = {inicio: 0}  
    costo_estimado = {inicio: heuristica(inicio, meta)}  

    while lista_abierta:
        nodo_actual = min(lista_abierta, key=lambda x: costo_estimado.get(x, float('inf')))

        if nodo_actual == meta:
            camino = []
            while nodo_actual in camino_desde:
                camino.append(nodo_actual)
                nodo_actual = camino_desde[nodo_actual]
            return camino[::-1]  

        lista_abierta.remove(nodo_actual)

        for movimiento_fila, movimiento_columna in movimientos:
            vecino = (nodo_actual[0] + movimiento_fila, nodo_actual[1] + movimiento_columna)
              
            if 0 <= vecino[0] < 10 and 0 <= vecino[1] < 10 and mapa[vecino] == 0:  
                costo_tentativo = costo_real[nodo_actual] + 1
                if vecino not in costo_real or costo_tentativo < costo_real[vecino]:
                    camino_desde[vecino] = nodo_actual
                    costo_real[vecino] = costo_tentativo
                    costo_estimado[vecino] = costo_tentativo + heuristica(vecino, meta)
                    if vecino not in lista_abierta:
                        lista_abierta.append(vecino)

    return None  



camino_optimo = algoritmo_a_estrella(mapa, inicio, meta)


if camino_optimo:
    for posicion in camino_optimo:
        mapa[posicion] = 2  
    print(mapa)
else:
    print("No hay camino disponible.")