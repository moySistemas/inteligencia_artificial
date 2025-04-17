import pygame
import numpy as np

# Configuraciones iniciales
pygame.init()
ANCHO_VENTANA = 500
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Fuente
FUENTE = pygame.font.SysFont('Arial', 12)

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

# Definición del mapa
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = col * ancho
        self.y = fila * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = None
        self.h = None
        self.f = None

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO
        self.g = self.h = self.f = None

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

        if self.g is not None and self.h is not None and self.f is not None:
            texto_g = FUENTE.render(f"g:{self.g}", True, NEGRO)
            texto_h = FUENTE.render(f"h:{self.h}", True, NEGRO)
            texto_f = FUENTE.render(f"f:{self.f}", True, NEGRO)
            ventana.blit(texto_g, (self.x + 2, self.y + 2))
            ventana.blit(texto_h, (self.x + 2, self.y + 15))
            ventana.blit(texto_f, (self.x + 2, self.y + 28))

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    x, y = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

# Función heurística - Distancia de Manhattan
def heuristica(nodo_actual, nodo_destino):
    return abs(nodo_actual[0] - nodo_destino[0]) + abs(nodo_actual[1] - nodo_destino[1])

# Función A*
def algoritmo_a_estrella(mapa, inicio, meta, grid):
    lista_abierta = [inicio]
    lista_cerrada = []
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

            # Imprimir lista cerrada
            print("Lista cerrada (nodos visitados):")
            for nodo in lista_cerrada:
                print(nodo)
            return camino[::-1]

        lista_abierta.remove(nodo_actual)
        if nodo_actual not in lista_cerrada:
            lista_cerrada.append(nodo_actual)

        for movimiento_fila, movimiento_col in movimientos:
            vecino = (nodo_actual[0] + movimiento_fila, nodo_actual[1] + movimiento_col)

            if 0 <= vecino[0] < len(mapa) and 0 <= vecino[1] < len(mapa) and mapa[vecino] == 0:
                costo_tentativo = costo_real[nodo_actual] + 1
                if vecino not in costo_real or costo_tentativo < costo_real[vecino]:
                    camino_desde[vecino] = nodo_actual
                    costo_real[vecino] = costo_tentativo
                    heur = heuristica(vecino, meta)
                    costo_estimado[vecino] = costo_tentativo + heur

                    fila, col = vecino
                    nodo_grid = grid[fila][col]
                    nodo_grid.g = costo_tentativo
                    nodo_grid.h = heur
                    nodo_grid.f = costo_estimado[vecino]

                    if vecino not in lista_abierta:
                        lista_abierta.append(vecino)

    print("No se encontró camino.")
    return None

# Configuración de la cuadrícula y movimientos
movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)
    inicio = None
    fin = None

    corriendo = True
    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    mapa = np.zeros((FILAS, FILAS), dtype=int)
                    for i in range(FILAS):
                        for j in range(FILAS):
                            if grid[i][j].es_pared():
                                mapa[i][j] = 1
                    camino = algoritmo_a_estrella(mapa, inicio.get_pos(), fin.get_pos(), grid)
                    if camino:
                        for fila, col in camino:
                            nodo = grid[fila][col]
                            if not nodo.es_inicio() and not nodo.es_fin():
                                nodo.color = VERDE
                    else:
                        print("No hay camino disponible.")

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
