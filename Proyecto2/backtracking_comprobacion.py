
"""Resolución de Sudoku con Backtracking y Comprobación hacia delante (Forward Checking)."""

from __future__ import annotations

import typing
from lectura_sudoku import es_posicion_valida, imprimir_tablero, leer_tablero, validar_tablero, _tamano_subcuadro

def buscar_celda_vacia(tablero: list[list[int]], n: int) -> tuple[int, int] | None:
    """Busca la siguiente celda vacía."""
    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                return fila, col
    return None

def calcular_dominio(tablero: list[list[int]], fila: int, col: int, n: int) -> list[int]:
    """Retorna los valores posibles para una celda vacía."""
    dominio = []
    for num in range(1, n + 1):
        if es_posicion_valida(tablero, fila, col, num, n):
            dominio.append(num)
    return dominio

def forward_checking_valido(tablero: list[list[int]], fila: int, col: int, n: int) -> bool:
    """
    Verifica los vecinos de (fila, col) que están vacíos. 
    Si alguno se queda sin valores posibles en su dominio, retorna False.
    """
    tam = _tamano_subcuadro(n)
    
    # Revisar vecinos en la misma fila y columna
    for i in range(n):
        # Misma fila
        if i != col and tablero[fila][i] == 0:
            if not calcular_dominio(tablero, fila, i, n):
                return False
        # Misma columna
        if i != fila and tablero[i][col] == 0:
            if not calcular_dominio(tablero, i, col, n):
                return False
                
    # Revisar en el mismo subcuadro
    inicio_fila = (fila // tam) * tam
    inicio_col = (col // tam) * tam
    for i in range(inicio_fila, inicio_fila + tam):
        for j in range(inicio_col, inicio_col + tam):
            if i != fila and j != col and tablero[i][j] == 0:
                if not calcular_dominio(tablero, i, j, n):
                    return False
                    
    return True

def solve_sudoku_fc(tablero: list[list[int]], n: int = 9, log_file: typing.TextIO | None = None, profundidad: int = 0) -> bool:
    """
    Resuelve el Sudoku usando Backtracking con Forward Checking.
    """
    if profundidad == 0 and not validar_tablero(tablero, n):
        return False

    celda = buscar_celda_vacia(tablero, n)
    if celda is None:
        if log_file:
            log_file.write("  " * profundidad + "-> ¡Tablero completado exitosamente!\n")
        return True # Ya está todo resuelto.

    fila, col = celda

    # Obtener el dominio de la celda vacía
    dominio = calcular_dominio(tablero, fila, col, n)
    
    if log_file:
        log_file.write("  " * profundidad + f"Evaluando celda ({fila}, {col}) - Dominio posible: {dominio}\n")

    for num in dominio:
        # 1. Asignar el valor
        if log_file:
            log_file.write("  " * profundidad + f"[*] Asignando {num} a ({fila}, {col})\n")
        tablero[fila][col] = num

        # 2. Forward checking
        if forward_checking_valido(tablero, fila, col, n):
            if log_file:
                log_file.write("  " * profundidad + f"    + Restricciones OK. Avanzando a la siguiente celda...\n")
            # 3. Solo exploramos si no vació el dominio de ningún vecino
            if solve_sudoku_fc(tablero, n, log_file, profundidad + 1):
                return True
        else:
            if log_file:
                log_file.write("  " * profundidad + f"    - FC Falló: Asignar {num} deja a un vecino en un callejón sin salida (Dominio vacío). Podando rama...\n")

        # Backtrack (deshacer)
        if log_file:
            log_file.write("  " * profundidad + f"[!] Backtracking en ({fila}, {col}): desasignando {num}\n")
        tablero[fila][col] = 0

    if log_file:
        log_file.write("  " * profundidad + f"<- No quedan opciones válidas para ({fila}, {col}). Regresando al nivel anterior.\n")
    return False

if __name__ == "__main__":
    tablero = leer_tablero("Proyecto2/sudoku_prueba.txt")
    print("Antes:")
    imprimir_tablero(tablero)

    if solve_sudoku_fc(tablero):
        print("\nSOLUCIÓN (Con Forward Checking):")
        imprimir_tablero(tablero)
    else:
        print("\nSin solución")
