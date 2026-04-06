"""Resolución de Sudoku por fuerza bruta pura."""

from __future__ import annotations

from lectura_sudoku import es_posicion_valida, imprimir_tablero, leer_tablero, validar_tablero


def _buscar_celda_vacia(tablero: list[list[int]], n: int) -> tuple[int, int] | None:
    """Encuentra la siguiente celda vacía (valor 0)."""
    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                return fila, col
    return None


def solve_sudoku_fb(tablero: list[list[int]], n: int = 9) -> bool:
    """
    Resuelve el Sudoku modificando el tablero in-place.

    Retorna True si encuentra solución y False si no existe solución.
    """
    if not validar_tablero(tablero, n):
        return False

    vacia = _buscar_celda_vacia(tablero, n)
    if vacia is None:
        return True

    fila, col = vacia

    for num in range(1, n + 1):
        if es_posicion_valida(tablero, fila, col, num, n):
            tablero[fila][col] = num

            if solve_sudoku_fb(tablero, n):
                return True

            tablero[fila][col] = 0

    return False


if __name__ == "__main__":
    tablero = leer_tablero("Proyecto2/sudoku_prueba.txt")
    print("Antes:")
    imprimir_tablero(tablero)

    if solve_sudoku_fb(tablero):
        print("\nSOLUCIÓN:")
        imprimir_tablero(tablero)
    else:
        print("\nSin solución")
