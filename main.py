from lectura import leer_matriz, matriz_grafo, encontrar_entrada
from busquedas import dfs, bfs, a_star
from hueristica import calculo_heuristica
import functools

# 1. Leer el laberinto
matriz = leer_matriz('laberinto.txt')

# 2. Convertir a grafo
grafo = {}
nodos = {}
nodos_inv = {}
entrada=encontrar_entrada(matriz)
grafo, nodos, nodos_inv, cont = matriz_grafo(grafo, nodos, nodos_inv, entrada, matriz, 0)

def encontrar_salida(matriz):
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            if val == 3:
                return (i, j)
salida = encontrar_salida(matriz)
# 3. Encontrar inicio y meta
inicio = nodos_inv[entrada]      # coordenada donde está el 2
meta = nodos_inv[salida]        # coordenada donde está el 3

# 4. Correr los algoritmos
camino_dfs = dfs(grafo, inicio, meta)
camino_bfs = bfs(grafo, inicio, meta)

heuristica = functools.partial(calculo_heuristica, nodos=nodos)
camino_astar = a_star(grafo, inicio, meta, heuristica)

# 5. Imprimir resultados
print("\n--- DFS ---")
print([nodos[n] for n in camino_dfs])

print("\n--- BFS ---")
print([nodos[n] for n in camino_bfs])

print("\n--- A* ---")
print([nodos[n] for n in camino_astar])