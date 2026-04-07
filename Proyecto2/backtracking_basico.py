"""Resolucion de Sudoku con backtracking basico."""

from __future__ import annotations

import math

from lectura_sudoku import imprimir_tablero, leer_tablero, validar_tablero


def buscar_celda_vacia(tablero: list[list[int]], n: int) -> tuple[int, int] | None:
    """Retorna la primera celda vacia encontrada o None si el tablero esta completo."""
    # Recorre el tablero en orden para ubicar la siguiente decision pendiente.
    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                return fila, col
    return None


def _indice_subcuadro(fila: int, col: int, tam_subcuadro: int) -> int:
    """Calcula a que subcuadro pertenece una celda."""
    return (fila // tam_subcuadro) * tam_subcuadro + (col // tam_subcuadro)


def _construir_restricciones(
    tablero: list[list[int]], n: int
) -> tuple[list[set[int]], list[set[int]], list[set[int]], list[tuple[int, int]], int]:
    """Prepara estructuras auxiliares para acelerar las verificaciones."""
    tam_subcuadro = math.isqrt(n)
    filas = [set() for _ in range(n)]
    columnas = [set() for _ in range(n)]
    subcuadros = [set() for _ in range(n)]
    vacias: list[tuple[int, int]] = []

    for fila in range(n):
        for col in range(n):
            valor = tablero[fila][col]
            if valor == 0:
                vacias.append((fila, col))
                continue

            filas[fila].add(valor)
            columnas[col].add(valor)
            subcuadros[_indice_subcuadro(fila, col, tam_subcuadro)].add(valor)

    return filas, columnas, subcuadros, vacias, tam_subcuadro


def _resolver_desde(
    tablero: list[list[int]],
    vacias: list[tuple[int, int]],
    indice: int,
    filas: list[set[int]],
    columnas: list[set[int]],
    subcuadros: list[set[int]],
    tam_subcuadro: int,
    n: int,
) -> bool:
    """Explora recursivamente las asignaciones validas restantes."""
    if indice == len(vacias):
        return True

    fila, col = vacias[indice]
    subcuadro = _indice_subcuadro(fila, col, tam_subcuadro)

    # Prueba candidatos consistentes con las restricciones acumuladas.
    for num in range(1, n + 1):
        if num in filas[fila] or num in columnas[col] or num in subcuadros[subcuadro]:
            continue

        tablero[fila][col] = num
        filas[fila].add(num)
        columnas[col].add(num)
        subcuadros[subcuadro].add(num)

        if _resolver_desde(tablero, vacias, indice + 1, filas, columnas, subcuadros, tam_subcuadro, n):
            return True

        # Si la rama falla, retrocede y deja la celda vacia.
        tablero[fila][col] = 0
        filas[fila].remove(num)
        columnas[col].remove(num)
        subcuadros[subcuadro].remove(num)

    return False


def solve_sudoku_bt(tablero: list[list[int]], n: int = 9) -> bool:
    """
    Resuelve el Sudoku usando backtracking basico.

    El algoritmo recorre las celdas vacias en orden y mantiene estructuras
    de restriccion para filas, columnas y subcuadros. Si una rama no conduce
    a una solucion, deshace el cambio y prueba el siguiente candidato.
    """
    if not validar_tablero(tablero, n):
        return False

    # Caso base: si no quedan celdas vacias, el tablero ya esta resuelto.
    if buscar_celda_vacia(tablero, n) is None:
        return True

    filas, columnas, subcuadros, vacias, tam_subcuadro = _construir_restricciones(tablero, n)
    return _resolver_desde(tablero, vacias, 0, filas, columnas, subcuadros, tam_subcuadro, n)


if __name__ == "__main__":
    # Bloque de prueba rapida para ejecutar este modulo por separado.
    tablero = leer_tablero("Proyecto2/sudoku_prueba.txt")
    print("Antes:")
    imprimir_tablero(tablero)

    if solve_sudoku_bt(tablero):
        print("\nSOLUCION:")
        imprimir_tablero(tablero)
    else:
        print("\nSin solucion")
