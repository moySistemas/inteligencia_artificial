# Proyectos IA - Documentación de proyectos
# Proyecto 1 - ALGORITMO A*


## Configuraciones iniciales

```python
# Configuraciones iniciales 
pygame.init()
ANCHO_VENTANA = 1000
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")
```
Primero se inicializa Pygame con pygame.init() para poder usar todas sus funciones. Luego se define el tamaño de la ventana con ANCHO_VENTANA, en este caso de 1000 píxeles por lado. Con ese tamaño, se crea la ventana donde se va a mostrar todo usando pygame.display.set_mode(). Finalmente, se le pone un título a la ventana con pygame.display.set_caption("Visualización de Nodos") para que sea más fácil identificarla.

- pygame.init(): Inicializa todos los módulos de Pygame.
- ANCHO_VENTANA: Define el tamaño de la ventana en píxeles.
- VENTANA: Crea la ventana de visualización con el tamaño especificado.
- pygame.display.set_caption("Visualización de Nodos"): Establece el título de la ventana.

## Fuente y Colores

```python
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
```
- Fuente: Define la fuente para mostrar el texto (tamaño 12)
- Colores: Se define como tuplas de valor RGB para varios colores como blanco, negro,gris,verde,rojo,narajana y púrpura.

## Función crear_grid

```python
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
```
Crea una cuadrícula (grid) de nodos. El número de nodos se determina por el número de filas y el ancho de la ventana. Cada nodo tiene un tamaño calculado como ancho // filas.

## Clase Nodo

```python
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
```
Representa un nodo en la cuadrícula. Cada nodo tiene:
- Posición (fila, col).
- Coordenadas x, y calculadas según su fila y columna.
- color: Color del nodo (por defecto blanco).
- Propiedades para el algoritmo A* (g, h, f), que son los costos del camino.

## Métodos de la clase Nodo

```python
    def get_pos(self):
        return self.fila, self.col
```
Devuelve la posición del nodo como tupla (fila, col)

```python
    def es_pared(self):
        return self.color == NEGRO
```
Verifica si el nodo es una pared (su color es negro).

```python
    def es_inicio(self):
        return self.color == NARANJA
```
Verifica si el nodo es el punto de inicio (su color es naranja).




