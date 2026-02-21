import ast
#funcion para leer la matriz
#recibe el parametro ruta que contiene el path al archivo con el laberinto
#la funcion lee linea por linea con ast.literal_eval aprovechando que el formato 
#ya es de una matriz y incluye la linea en la variable matriz
#la funcion devuelve dicha matriz que contiene los datos del archivo
def leer_matriz(ruta):
    matriz = []
    with open(ruta, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                fila = ast.literal_eval(linea)
                matriz.append(fila)
    return matriz

 
#funcion para encontrar las direcciones validas de una celda
#recibe la matriz que codifica el laberinto y las fila y columna de la celda a analizar
#la funcion revisa para la celda izquierda, derecha, arriba y abajo de la analizada
#verifica si es una pared, si se sale del laberinto o es una celda de camino
#devuelve las cordenadas de las direcciones hacia donde hay camino
def get_dirs_validas(matriz, fil, col):
    filas, cols = len(matriz), len(matriz[0])
    dirs = []
    for df, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        nf, nc = fil+df, col+dc
        if 0 <= nf < filas and 0 <= nc < cols and matriz[nf][nc] != 1:
            dirs.append((nf, nc))  
    return dirs

#funcion para convertir de matriz a grafo
#recibe el grafo que se lleva, los nodos que se llevan y sus inversos
#las coordenadas a analizar, la matriz y un conteo de nodos
#la funcion verifica si es un nodo de desicion, la entrada o la salida y empieza a verificar las direcciones validas
#desde el primer nodo, luego recorre hasta encontrar el siguiente nodo y asi sucesivamente de manera recursiva hasta terminar de crear los nodos 
#y incluirlos tanto en el grafo como en la inversa de los nodos y aumentar el numero del contador
#la funcion devuelve el grafo, los nodos, los nodos inversos y el contador
def matriz_grafo(grafo, nodos, nodos_inv, coord, matriz, cont):
    filas = len(matriz)
    cols = len(matriz[0])
    fil, col = coord  
    print("nodo analizado:"+str(fil)+","+str(col)+"           "+str(matriz[fil][col]))
    dirs_validas = get_dirs_validas(matriz, fil, col)
    rutas = len(dirs_validas)

    es_nodo = rutas != 2 or matriz[fil][col] in (2, 3)

    if not es_nodo:
        print("no es nodo")
        return grafo, nodos, nodos_inv, cont

    if (fil, col) not in nodos_inv:
        print("nodo nuevo")
        nodos[cont] = (fil, col)
        nodos_inv[(fil, col)] = cont
        grafo[cont] = []
        cont += 1

    nodo_actual = nodos_inv[(fil, col)]

    for siguiente in dirs_validas:
        nf, nc = siguiente
        prev = (fil, col)
        print("siguiente direccion:"+str(nf)+","+str(nc)+"           "+str(matriz[nf][nc]))
        while 0 <= nf < filas and 0 <= nc < cols and matriz[nf][nc] != 1:
            print("entra")
            dirs_celda = get_dirs_validas(matriz, nf, nc)

            if len(dirs_celda) != 2 or matriz[nf][nc] in (2, 3):
                if (nf, nc) not in nodos_inv:
                    grafo, nodos, nodos_inv, cont = matriz_grafo(
                        grafo, nodos, nodos_inv, (nf, nc), matriz, cont
                    )
                if (nf, nc) in nodos_inv:
                    nodo_vecino = nodos_inv[(nf, nc)]
                    if nodo_vecino not in grafo[nodo_actual]:
                        grafo[nodo_actual].append(nodo_vecino)
                        grafo[nodo_vecino].append(nodo_actual)
                break

            
            siguiente_celdas = [c for c in dirs_celda if c != prev]
            if not siguiente_celdas:
                break
            prev = (nf, nc)
            nf, nc = siguiente_celdas[0]
            print("siguiente direccion caminando:"+str(nf)+","+str(nc)+"           "+str(matriz[nf][nc]))

    return grafo, nodos, nodos_inv, cont


#leemos el archivo del laberinto
matriz = leer_matriz('laberinto.txt')
grafo = {}
nodos = {}
nodos_inv = {}


cont = 0

#convertimos la matriz a grafo
grafo, nodos, nodos_inv, cont = matriz_grafo(grafo, nodos, nodos_inv, (0,0), matriz, cont)

print(f"Nodos: {nodos}")
print(f"Grafo: {grafo}")

num_nodos = len(nodos)
matriz_adyacencia = [[0] * num_nodos for _ in range(num_nodos)]
#convertimos de un grafo en set a un grafo de matriz de adjacencia
for nodo, vecinos in grafo.items():
    for vecino in vecinos:
        matriz_adyacencia[nodo][vecino] = 1
        matriz_adyacencia[vecino][nodo] = 1

for fila in matriz_adyacencia:
    print(fila)