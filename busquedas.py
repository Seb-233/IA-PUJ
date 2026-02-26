from collections import deque
import heapq

# funcion auxiliar para obtener vecinos y pesos desde la matriz de adyacencia
# recibe la matriz de adyacencia y el nodo actual
# devuelve una lista de tuplas (vecino, peso) donde peso > 0 indica conexion
def get_vecinos(matriz_adyacencia, nodo):
    vecinos = []
    for i, peso in enumerate(matriz_adyacencia[nodo]):
        if peso > 0:
            vecinos.append((i, peso))
    return vecinos


# DFS - Búsqueda Primero en Profundidad
# recibe la matriz de adyacencia con pesos, el nodo inicio y el nodo meta
def dfs(matriz_adyacencia, inicio, meta):
    stack = [(inicio, [inicio])]  # PILA: el último elemento que entra es el primero que sale (LIFO)
    visitados = set([inicio])

    while stack:
        nodo, camino = stack.pop()  # pop() saca el ultimo elemento de la lista (LIFO)

        if nodo == meta:
            return camino

        for vecino, peso in get_vecinos(matriz_adyacencia, nodo):  # obtenemos vecinos y pesos de la matriz
            if vecino not in visitados:
                visitados.add(vecino)
                stack.append((vecino, camino + [vecino]))

    return None


# BFS - Búsqueda Primero en Anchura
# recibe la matriz de adyacencia con pesos, el nodo inicio y el nodo meta
def bfs(matriz_adyacencia, inicio, meta):
    queue = deque([(inicio, [inicio])])  # COLA: el primero que entra es el primero que sale (FIFO)
    visitados = set([inicio])

    while queue:
        nodo, camino = queue.popleft()  # popleft() saca el PRIMER elemento de la cola (FIFO)

        if nodo == meta:
            return camino

        for vecino, peso in get_vecinos(matriz_adyacencia, nodo):  # obtenemos vecinos y pesos de la matriz
            if vecino not in visitados:
                visitados.add(vecino)
                queue.append((vecino, camino + [vecino]))

    return None


# A* - Búsqueda Informada
# recibe la matriz de adyacencia con pesos, el nodo inicio, el nodo meta y la heuristica
# usa el peso real de la matriz en lugar de costo uniforme = 1
def a_star(matriz_adyacencia, inicio, meta, heuristica):

    cola_prioridad = []  # heapq mantiene ordenado por prioridad (f(n))
    heapq.heappush(cola_prioridad, (0, inicio, [inicio]))

    costos_g = {inicio: 0}
    visitados = set()

    while cola_prioridad:
        f_actual, nodo, camino = heapq.heappop(cola_prioridad)  # Se extrae el nodo con menor f(n)

        if nodo in visitados:
            continue

        visitados.add(nodo)

        if nodo == meta:
            return camino

        for vecino, peso in get_vecinos(matriz_adyacencia, nodo):  # obtenemos vecinos y pesos de la matriz
            costo_g_nuevo = costos_g[nodo] + peso  # usamos el peso real de la matriz

            # Si encontramos mejor camino al vecino
            if vecino not in costos_g or costo_g_nuevo < costos_g[vecino]:
                costos_g[vecino] = costo_g_nuevo

                # f(n) = g(n) + h(n)
                f_nuevo = costo_g_nuevo + heuristica(vecino, meta)

                heapq.heappush(
                    cola_prioridad,
                    (f_nuevo, vecino, camino + [vecino])
                )

    return None