def heuristica_manhattan(nodo, meta, nodos=None):
    """
    Calcula la distancia Manhattan entre `nodo` y `meta`.

    - Si `nodo` y `meta` son tuplas (fila, col), calcula directo.
    - Si son IDs numéricos, se puede pasar `nodos` (id -> (fila, col)).
    """
    if nodos is not None:
        nodo = nodos[nodo]
        meta = nodos[meta]

    fila_nodo, col_nodo = nodo
    fila_meta, col_meta = meta
    return abs(fila_nodo - fila_meta) + abs(col_nodo - col_meta)


def calculo_heuristica(nodo, meta, nodos=None):
    return heuristica_manhattan(nodo, meta, nodos)
