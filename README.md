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

```python
    def es_fin(self):
        return self.color == PURPURA
```
Verifica si el nodo es el punto de fin (su color es púrpura).

```python
    def restablecer(self):
        self.color = BLANCO
        self.g = self.h = self.f = None
```
Resetea las propiedades del nodo a sus valores iniciales.

```python
 def hacer_inicio(self):
        self.color = NARANJA
```
Establece el color del nodo como el color de inicio (naranja).

```python
    def hacer_pared(self):
        self.color = NEGRO
```
 Establece el color del nodo como pared (negro).

 ```python
    def hacer_fin(self):
        self.color = PURPURA
```
Establece el color del nodo como el color de fin (púrpura).


```python
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
```

Dibuja el nodo en la ventana con el color actual.


## Funciones para dibujar la cuadrícula

```python
def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))
```
Dibuja las líneas de la cuadrícula (en gris) sobre la ventana.


```python
def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()
```
Rellena la ventana con el color blanco, dibuja todos los nodos en la cuadrícula, luego dibuja la cuadrícula y actualiza la pantalla.


## Obtener la posición del clic

```python
def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    x, y = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col
```
Convierte la posición del clic del ratón en la ventana en coordenadas de la cuadrícula.


## El algoritmo A*

###  Definición de A en el código*

El algoritmo A* se encuentra en la función algoritmo_a_estrella. La idea principal de A* es explorar los nodos cercanos al nodo actual y usar una combinación de costos:

- Costo real (g): El costo desde el nodo inicial hasta el nodo actual.
- Costo estimado (h): La estimación de la distancia desde el nodo actual hasta el nodo objetivo (utilizando una heurística, en este caso, la distancia de Manhattan).
- Costo total (f): La suma de g + h. Este valor se usa para determinar cuál nodo explorar a continuación.

A* busca minimizar la combinación de estos valores (f), con el objetivo de encontrar el camino más corto desde el nodo de inicio hasta el nodo de fin.

### Funcionamiento del algoritmo A*

La función algoritmo_a_estrella toma como parámetros:

- mapa: Un arreglo 2D que representa el mapa del entorno, donde cada celda es 0 (camino libre) o 1 (pared).
- inicio: El nodo de inicio (coordenadas fila, columna).
- meta: El nodo objetivo (meta).
- grid: La cuadrícula completa de nodos.

Dentro de la función se manejan varias listas y diccionarios para el cálculo:

- lista_abierta: Lista de nodos que aún no han sido evaluados.
- lista_cerrada: Lista de nodos que ya han sido evaluados.
- camino_desde: Diccionario que guarda de qué nodo proviene cada nodo en el camino (útil para reconstruir el camino final).
- costo_real: Diccionario que almacena el costo real g de cada nodo.
- costo_estimado: Diccionario que almacena el costo estimado f de cada nodo.

### Búsqueda en la lista abierta

1. Dentro de un bucle while, el algoritmo A* realiza lo siguiente:
Seleccionar el nodo con el menor costo estimado f: De todos los nodos en lista_abierta, selecciona el nodo que tiene el valor más bajo de f (costo total). Este nodo es el más prometedor para encontrar un camino hacia el objetivo.

```python
nodo_actual = min(lista_abierta, key=lambda x: costo_estimado.get(x, float('inf')))
```

2. Comprobar si se ha llegado al objetivo: Si el nodo actual es igual al nodo de meta, significa que hemos encontrado un camino. Se reconstruye el camino desde el nodo de inicio hasta la meta, siguiendo los nodos almacenados en camino_desde.

3. Mover el nodo a la lista cerrada: Si el nodo actual no es la meta, se mueve a la lista_cerrada para marcarlo como visitado y evitar recorrerlo de nuevo.

```python
        lista_abierta.remove(nodo_actual)
        if nodo_actual not in lista_cerrada:
            lista_cerrada.append(nodo_actual)
```

4. Explorar los vecinos: A continuación, el algoritmo explora los vecinos del nodo actual (nodos adyacentes) siguiendo los movimientos definidos en la lista movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]. Los vecinos son evaluados en función de su costo.

```python
for movimiento_fila, movimiento_col in movimientos:
            vecino = (nodo_actual[0] + movimiento_fila, nodo_actual[1] + movimiento_col)
```
Si el vecino es válido (dentro de los límites del mapa y no es una pared), se calcula el costo tentativo (costo_tentativo) para llegar al vecino desde el nodo actual. Si este costo es menor que el costo previamente registrado para ese vecino, se actualiza el costo y la información del nodo.

```python
   if 0 <= vecino[0] < len(mapa) and 0 <= vecino[1] < len(mapa) and mapa[vecino] == 0:
                costo_tentativo = costo_real[nodo_actual] + 1
                if vecino not in costo_real or costo_tentativo < costo_real[vecino]:
                    camino_desde[vecino] = nodo_actual
                    costo_real[vecino] = costo_tentativo
                    heur = heuristica(vecino, meta)
                    costo_estimado[vecino] = costo_tentativo + heur
```
Heurística: La heurística usada es la distancia de Manhattan:

```python
def heuristica(nodo_actual, nodo_destino):
    return abs(nodo_actual[0] - nodo_destino[0]) + abs(nodo_actual[1] - nodo_destino[1])
```

Esta fórmula calcula la distancia total de las celdas en un plano de rejilla considerando solo los movimientos en línea recta horizontal y vertical (sin diagonales).

5. Actualizar la cuadrícula visualmente: Cada vez que se encuentra un vecino válido, se actualizan los valores de g, h, y f para los nodos en la cuadrícula. Esto es útil para visualizarlos en la interfaz gráfica.

```python
fila, col = vecino
nodo_grid = grid[fila][col]
nodo_grid.g = costo_tentativo
nodo_grid.h = heur
nodo_grid.f = costo_estimado[vecino]
```

6. Agregar a la lista abierta: Si el vecino no está en la lista abierta, se agrega para que sea evaluado más tarde.

```python
if vecino not in lista_abierta:
    lista_abierta.append(vecino)
```

7. No se encuentra camino: Si se termina el bucle y no se ha encontrado un camino hacia el nodo de meta, se devuelve None.

```python
print("No se encontró camino.")
return None
```

### Reconstrucción del camino
Cuando el algoritmo A* llega a la meta, reconstruye el camino a partir de los nodos que se han visitado, usando el diccionario camino_desde. El camino es una lista de nodos, y luego se invierte para que quede desde el inicio hasta la meta.


## Función principal (main)

```python
def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)
    inicio = None
    fin = None
```

Inicializa el juego. Permite que el usuario haga clic para establecer los puntos de inicio y fin, y colocar paredes. Al presionar la barra espaciadora, ejecuta el algoritmo A*.

## Ejecutar el programa
```python
main(VENTANA, ANCHO_VENTANA)
```
Llama a la función main para ejecutar la visualización y el algoritmo A*.
