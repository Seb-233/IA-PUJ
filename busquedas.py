from collections import deque
import heapq

# funcion auxiliar para obtener vecinos y pesos desde la matriz de adyacencia
# recibe la matriz de adyacencia y el id del nodo actual
# la funcion recorre la fila del nodo en la matriz y busca celdas con valor mayor a 0
# ya que un valor de 0 indica que no hay conexion entre esos dos nodos
# devuelve una lista de tuplas (vecino, peso) con todos los nodos conectados al nodo actual
def get_vecinos(matriz_adyacencia, nodo):
    vecinos = []
    for i, peso in enumerate(matriz_adyacencia[nodo]):
        if peso > 0:
            vecinos.append((i, peso))
    return vecinos


# funcion para buscar el camino usando DFS - Busqueda Primero en Profundidad
# recibe la matriz de adyacencia con pesos, el nodo inicio y el nodo meta
# la funcion usa una pila donde el ultimo elemento que entra es el primero que sale (LIFO)
# desde el nodo inicio expande el nodo mas reciente agregado a la pila
# y marca cada nodo visitado para no procesarlo dos veces
# devuelve el camino como lista de ids de nodos de decision desde inicio hasta meta
# devuelve None si no existe camino
def dfs(matriz_adyacencia, inicio, meta):
    stack = [(inicio, [inicio])]
    visitados = set([inicio])
    while stack:
        nodo, camino = stack.pop()
        if nodo == meta:
            return camino
        for vecino, peso in get_vecinos(matriz_adyacencia, nodo):
            if vecino not in visitados:
                visitados.add(vecino)
                stack.append((vecino, camino + [vecino]))
    return None


# funcion para buscar el camino usando BFS - Busqueda Primero en Anchura
# recibe la matriz de adyacencia con pesos, el nodo inicio y el nodo meta
# la funcion usa una cola donde el primero que entra es el primero que sale (FIFO)
# desde el nodo inicio expande nivel por nivel todos los vecinos accesibles
# y marca cada nodo visitado para no procesarlo dos veces
# al ser BFS garantiza encontrar el camino con menos nodos de decision intermedios
# devuelve el camino como lista de ids de nodos de decision desde inicio hasta meta
# devuelve None si no existe camino
def bfs(matriz_adyacencia, inicio, meta):
    queue = deque([(inicio, [inicio])])
    visitados = set([inicio])
    while queue:
        nodo, camino = queue.popleft()
        if nodo == meta:
            return camino
        for vecino, peso in get_vecinos(matriz_adyacencia, nodo):
            if vecino not in visitados:
                visitados.add(vecino)
                queue.append((vecino, camino + [vecino]))
    return None


# funcion para buscar el camino usando A* con conteo de nodos expandidos
# recibe la matriz de adyacencia con pesos, el nodo inicio, el nodo meta y la funcion heuristica
# la funcion usa una cola de prioridad ordenada por f(n) = g(n) + h(n)
# donde g(n) es el costo acumulado real usando los pesos de la matriz
# y h(n) es la distancia manhattan estimada hasta la meta
# en cada iteracion extrae el nodo con menor f(n) y expande sus vecinos
# si encuentra un camino mas barato a un vecino actualiza su costo y lo reencola
# ademas lleva un contador de cuantos nodos son realmente expandidos (salen de la cola)
# devuelve una tupla con el camino como lista de ids de nodos de decision y el numero de nodos expandidos
# devuelve (None, nodos_expandidos) si no existe camino
def a_star_con_conteo(matriz_adyacencia, inicio, meta, heuristica):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio, [inicio]))
    costos_g = {inicio: 0}
    visitados = set()
    nodos_expandidos = 0
    while cola_prioridad:
        f_actual, nodo, camino = heapq.heappop(cola_prioridad)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        nodos_expandidos += 1
        if nodo == meta:
            return camino, nodos_expandidos
        for vecino, peso in get_vecinos(matriz_adyacencia, nodo):
            costo_g_nuevo = costos_g[nodo] + peso
            if vecino not in costos_g or costo_g_nuevo < costos_g[vecino]:
                costos_g[vecino] = costo_g_nuevo
                f_nuevo = costo_g_nuevo + heuristica(vecino, meta)
                heapq.heappush(cola_prioridad, (f_nuevo, vecino, camino + [vecino]))
    return None, nodos_expandidos