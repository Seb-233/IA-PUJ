from lectura import leer_matriz, matriz_grafo, encontrar_entrada, encontrar_salida , reconstruir_ruta
from busquedas import dfs, bfs, a_star_con_conteo 
from hueristica import calculo_heuristica
import functools

# 1. Leer el laberinto
matriz = leer_matriz('laberinto.txt')

# 2. Encontrar entrada y salida
entrada = encontrar_entrada(matriz)
salida  = encontrar_salida(matriz)

# 3. Convertir a grafo con pesos
grafo     = {}
nodos     = {}
nodos_inv = {}
grafo, nodos, nodos_inv, cont = matriz_grafo(grafo, nodos, nodos_inv, entrada, matriz, 0)

# 4. Construir matriz de adyacencia con pesos (0 = sin conexion)
num_nodos = len(nodos)
matriz_adyacencia = [[0] * num_nodos for _ in range(num_nodos)]

for nodo, vecinos in grafo.items():
    for vecino, peso in vecinos:
        matriz_adyacencia[nodo][vecino] = peso
        matriz_adyacencia[vecino][nodo] = peso

# 5. Imprimir matriz de adyacencia con encabezados para facilitar la lectura
print("\nMatriz de adyacencia (pesos = pasos entre nodos):")
print("     " + "  ".join(f"{i:2}" for i in range(num_nodos)))
print("     " + "----" * num_nodos)
for i, fila in enumerate(matriz_adyacencia):
    print(f"{i:2} |  " + "  ".join(f"{v:2}" for v in fila))

# 6. Encontrar inicio y meta usando las coordenadas de entrada y salida
inicio = nodos_inv[entrada]  # coordenada donde está el 2
meta   = nodos_inv[salida]   # coordenada donde está el 3

# 7. Correr los algoritmos usando la matriz de adyacencia
camino_dfs = dfs(matriz_adyacencia, inicio, meta)
camino_bfs = bfs(matriz_adyacencia, inicio, meta)
heuristica = functools.partial(calculo_heuristica, nodos=nodos)
camino_astar, nodos_exp = a_star_con_conteo(matriz_adyacencia, inicio, meta, heuristica)

# 5. reconstruir ruta completa de A*
ruta_completa = reconstruir_ruta(camino_astar, nodos, matriz)

# 6. imprimir resultados
print("\n--- DFS (nodos de decision) ---")
print([nodos[n] for n in camino_dfs])

print("\n--- BFS (nodos de decision) ---")
print([nodos[n] for n in camino_bfs])

print("\n--- A* (nodos de decision) ---")
print([nodos[n] for n in camino_astar])

print("\n--- A* ruta completa celda por celda ---")
print(ruta_completa)

print("\n--- Comparativa de rendimiento ---")
print(f"Nodos expandidos por A* macro: {nodos_exp}")
print(f"Total de nodos en el grafo:    {num_nodos}")