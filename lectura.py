import ast

#funcion para leer la matriz
#recibe el parametro ruta que contiene el path al archivo con el laberinto
#la funcion lee linea por linea con ast.literal_eval aprovechando que el formato 
#ya es de una matriz e incluye la linea en la variable matriz
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
#ademas cuenta los pasos entre nodos para asignar el peso de cada conexion
#la funcion devuelve el grafo, los nodos, los nodos inversos y el contador
def matriz_grafo(grafo, nodos, nodos_inv, coord, matriz, cont):
    filas = len(matriz)
    cols = len(matriz[0])
    fil, col = coord
    dirs_validas = get_dirs_validas(matriz, fil, col)
    rutas = len(dirs_validas)

    es_nodo = rutas != 2 or matriz[fil][col] in (2, 3)

    if not es_nodo:
        return grafo, nodos, nodos_inv, cont

    if (fil, col) not in nodos_inv:
        print("Creando nodo {} en coordenada ({}, {})".format(cont, fil, col))
        nodos[cont] = (fil, col)
        nodos_inv[(fil, col)] = cont
        grafo[cont] = []
        cont += 1

    nodo_actual = nodos_inv[(fil, col)]

    for siguiente in dirs_validas:
        nf, nc = siguiente
        prev = (fil, col)
        pasos = 1  # iniciamos el conteo de pasos desde el nodo actual

        while 0 <= nf < filas and 0 <= nc < cols and matriz[nf][nc] != 1:
            dirs_celda = get_dirs_validas(matriz, nf, nc)

            if len(dirs_celda) != 2 or matriz[nf][nc] in (2, 3):
                if (nf, nc) not in nodos_inv:
                    grafo, nodos, nodos_inv, cont = matriz_grafo(
                        grafo, nodos, nodos_inv, (nf, nc), matriz, cont
                    )
                if (nf, nc) in nodos_inv:
                    nodo_vecino = nodos_inv[(nf, nc)]
                    # verificamos que la conexion no exista ya y agregamos con su peso
                    ya_conectado = any(v == nodo_vecino for v, _ in grafo[nodo_actual])
                    if not ya_conectado:
                        grafo[nodo_actual].append((nodo_vecino, pasos))
                        grafo[nodo_vecino].append((nodo_actual, pasos))
                break

            siguiente_celdas = [c for c in dirs_celda if c != prev]
            if not siguiente_celdas:
                break
            prev = (nf, nc)
            nf, nc = siguiente_celdas[0]
            pasos += 1  # sumamos un paso cada vez que avanzamos por el pasillo

    return grafo, nodos, nodos_inv, cont


#funcion para encontrar la entrada del laberinto
#recibe la matriz y busca la celda con valor 2
#devuelve las coordenadas de la entrada
#lanza un error si no se encuentra
def encontrar_entrada(matriz):
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            if val == 2:
                return (i, j)



#funcion para encontrar la salida del laberinto
#recibe la matriz y busca la celda con valor 3
#devuelve las coordenadas de la salida
#lanza un error si no se encuentra
def encontrar_salida(matriz):
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            if val == 3:
                return (i, j)

# funcion para reconstruir la ruta completa desde el camino compacto de nodos de decision
# recibe el camino compacto como lista de ids de nodos de decision,
# el diccionario nodos (id -> coordenada) y la matriz del laberinto
# la funcion recorre cada par de nodos consecutivos del camino compacto
# y usa BFS para encontrar todas las celdas intermedias del corredor entre ellos
# de esta forma expande el camino de nodos de decision a todos los pasos celda por celda
# evita duplicar el nodo de union entre tramos consecutivos
# devuelve la ruta completa como lista de coordenadas (fila, columna) desde la entrada hasta la salida
def reconstruir_ruta(camino_compacto, nodos, matriz):
    ruta_completa = []

    for i in range(len(camino_compacto) - 1):
        coord_actual = nodos[camino_compacto[i]]
        coord_siguiente = nodos[camino_compacto[i + 1]]

        # usamos BFS para encontrar el camino entre los dos nodos de decision
        cola = [(coord_actual, [coord_actual])]
        visitados = {coord_actual}

        tramo = None
        while cola:
            (fil, col), camino_tramo = cola.pop(0)

            if (fil, col) == coord_siguiente:
                tramo = camino_tramo
                break

            for nf, nc in get_dirs_validas(matriz, fil, col):
                if (nf, nc) not in visitados:
                    visitados.add((nf, nc))
                    cola.append(((nf, nc), camino_tramo + [(nf, nc)]))

        if tramo:
            # evitamos duplicar el nodo de union entre tramos
            if ruta_completa and ruta_completa[-1] == tramo[0]:
                ruta_completa.extend(tramo[1:])
            else:
                ruta_completa.extend(tramo)

    return ruta_completa