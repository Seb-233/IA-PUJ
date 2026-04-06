"""Funciones base para leer, validar e imprimir tableros de Sudoku."""

from __future__ import annotations

import ast
import math
from pathlib import Path


def _tamano_subcuadro(n: int) -> int:
    raiz = math.isqrt(n)
    if raiz * raiz != n:
        raise ValueError(f"El tamaño {n} no permite subcuadros cuadrados.")
    return raiz


def _es_matriz(tablero: object, n: int) -> bool:
    return (
        isinstance(tablero, list)
        and len(tablero) == n
        and all(isinstance(fila, list) and len(fila) == n for fila in tablero)
    )


def leer_tablero(ruta: str, n: int = 9) -> list[list[int]]:
    """
    Lee un tablero n x n desde un archivo de texto.

    Cada línea del archivo debe representar una fila como una lista de Python,
    por ejemplo: [5, 3, 0, 0, 7, 0, 0, 0, 0]
    """
    _tamano_subcuadro(n)

    tablero = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                fila = ast.literal_eval(linea)
                tablero.append(fila)

    if not validar_tablero(tablero, n):
        raise ValueError("El archivo no representa un tablero válido.")
    return tablero


def validar_fila(tablero: list[list[int]], fila: int, num: int, n: int) -> bool:
    for col in range(n):
        if tablero[fila][col] == num:
            return False
    return True


def validar_columna(tablero: list[list[int]], col: int, num: int, n: int) -> bool:
    for fila in range(n):
        if tablero[fila][col] == num:
            return False
    return True


def validar_cuadro(tablero: list[list[int]], fila: int, col: int, num: int, n: int) -> bool:
    tam = _tamano_subcuadro(n)
    inicio_fila = (fila // tam) * tam
    inicio_col = (col // tam) * tam

    for i in range(inicio_fila, inicio_fila + tam):
        for j in range(inicio_col, inicio_col + tam):
            if tablero[i][j] == num:
                return False
    return True


def es_posicion_valida(tablero: list[list[int]], fila: int, col: int, num: int, n: int) -> bool:
    if not (0 <= fila < n and 0 <= col < n):
        return False
    if not (1 <= num <= n):
        return False
    if tablero[fila][col] != 0:
        return False

    return (
        validar_fila(tablero, fila, num, n)
        and validar_columna(tablero, col, num, n)
        and validar_cuadro(tablero, fila, col, num, n)
    )


def validar_tablero(tablero: list[list[int]], n: int) -> bool:
    _tamano_subcuadro(n)

    if not _es_matriz(tablero, n):
        return False

    for fila in tablero:
        for valor in fila:
            if not isinstance(valor, int) or not (0 <= valor <= n):
                return False

    for fila in range(n):
        vistos = set()
        for col in range(n):
            valor = tablero[fila][col]
            if valor == 0:
                continue
            if valor in vistos:
                return False
            vistos.add(valor)

    for col in range(n):
        vistos = set()
        for fila in range(n):
            valor = tablero[fila][col]
            if valor == 0:
                continue
            if valor in vistos:
                return False
            vistos.add(valor)

    tam = _tamano_subcuadro(n)
    for inicio_fila in range(0, n, tam):
        for inicio_col in range(0, n, tam):
            vistos = set()
            for fila in range(inicio_fila, inicio_fila + tam):
                for col in range(inicio_col, inicio_col + tam):
                    valor = tablero[fila][col]
                    if valor == 0:
                        continue
                    if valor in vistos:
                        return False
                    vistos.add(valor)

    return True


def imprimir_tablero(tablero: list[list[int]]) -> None:
    n = len(tablero)
    tam = _tamano_subcuadro(n)
    ancho = len(str(n))

    separador_bloque = "-".join(["-" * ((ancho + 2) * tam - 1)] * tam)

    for i, fila in enumerate(tablero):
        if i > 0 and i % tam == 0:
            print(separador_bloque)

        partes = []
        for j, valor in enumerate(fila):
            celda = "." if valor == 0 else str(valor)
            partes.append(celda.rjust(ancho))
            if (j + 1) % tam == 0 and j < n - 1:
                partes.append("|")
        print(" ".join(partes))


if __name__ == "__main__":
    ruta_prueba = "Proyecto2/sudoku_prueba.txt"
    tablero = leer_tablero(ruta_prueba)
    print(f"Prueba desde archivo: {ruta_prueba}")
    print("Tablero válido:", validar_tablero(tablero, 9))
    imprimir_tablero(tablero)