"""Resolucion de Sudoku con backtracking basico."""

from __future__ import annotations

from lectura_sudoku import es_posicion_valida, imprimir_tablero, leer_tablero, validar_tablero


def buscar_celda_vacia(tablero: list[list[int]], n: int) -> tuple[int, int] | None:
    """Retorna la primera celda vacia encontrada o None si el tablero esta completo."""
    # Recorre el tablero en orden para ubicar la siguiente decision pendiente.
    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                return fila, col
    return None


def solve_sudoku_bt(tablero: list[list[int]], n: int = 9) -> bool:
    """
    Resuelve el Sudoku usando backtracking basico.

    El algoritmo prueba un numero valido en una celda vacia y avanza
    recursivamente. Si una rama no conduce a una solucion, deshace el
    cambio y prueba el siguiente candidato.
    """
    if not validar_tablero(tablero, n):
        return False

    # Caso base: si no quedan celdas vacias, el tablero ya esta resuelto.
    celda = buscar_celda_vacia(tablero, n)
    if celda is None:
        return True

    fila, col = celda

    # Prueba cada candidato posible para la celda actual.
    for num in range(1, n + 1):
        if not es_posicion_valida(tablero, fila, col, num, n):
            continue

        # Extiende una solucion parcial valida.
        tablero[fila][col] = num

        if solve_sudoku_bt(tablero, n):
            return True

        # Si la rama falla, retrocede y deja la celda vacia.
        tablero[fila][col] = 0

    return False


if __name__ == "__main__":
    # Bloque de prueba rapida para ejecutar este modulo por separado.
    tablero = leer_tablero("sudoku_prueba.txt")
    print("Antes:")
    imprimir_tablero(tablero)

    if solve_sudoku_bt(tablero):
        print("\nSOLUCION:")
        imprimir_tablero(tablero)
    else:
        print("\nSin solucion")
