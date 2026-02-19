from collections import deque
import heapq

# DFS - Búsqueda Primero en Profundidad
def dfs(grafo, inicio, meta):
    stack = [(inicio, [inicio])]   # PILA: el último elemento que entra es el primero que sale (LIFO)
    visitados = set([inicio])

    while stack:
        nodo, camino = stack.pop() # pop() saca el ultimo elemento de la lista (LIFO)

        if nodo == meta:
            return camino

        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                stack.append((vecino, camino + [vecino]))

    return None

# BFS - Búsqueda Primero en Anchura
def bfs(grafo, inicio, meta):
    queue = deque([(inicio, [inicio])]) # COLA: el primero que entra es el primero que sale (FIFO)
    visitados = set([inicio])

    while queue:
        nodo, camino = queue.popleft() # popleft() saca el PRIMER elemento de la cola (FIFO) 

        if nodo == meta:
            return camino

        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                queue.append((vecino, camino + [vecino]))

    return None

# A* - Búsqueda Informada
def a_star(grafo, inicio, meta, heuristica):
    
    cola_prioridad = [] # heapq mantiene ordenado por prioridad (f(n))
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

        for vecino in grafo.get(nodo, []):
            costo_g_nuevo = costos_g[nodo] + 1  # costo uniforme = 1

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