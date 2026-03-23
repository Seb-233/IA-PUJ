"""Funciones base para leer, validar e imprimir tableros de Sudoku."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable


def _tamano_subcuadro(n: int) -> int:
    """Retorna el tamaño del subcuadro y valida que n sea un cuadrado perfecto."""
    raiz = math.isqrt(n)
    if raiz * raiz != n:
        raise ValueError(f"El tamaño {n} no permite subcuadros cuadrados.")
    return raiz


def _es_matriz(tablero: object, n: int) -> bool:
    """Verifica si el objeto tiene forma de matriz n x n."""
    return (
        isinstance(tablero, list)
        and len(tablero) == n
        and all(isinstance(fila, list) and len(fila) == n for fila in tablero)
    )


def _normalizar_valores(valores: Iterable[object], total: int) -> list[int]:
    """Convierte una secuencia de valores a enteros y valida la longitud."""
    lista = list(valores)
    if len(lista) != total:
        raise ValueError(f"Se esperaban {total} valores y se recibieron {len(lista)}.")

    resultado = []
    for valor in lista:
        try:
            resultado.append(int(valor))
        except (TypeError, ValueError) as error:
            raise ValueError(f"Valor no convertible a entero: {valor!r}") from error
    return resultado


def leer_tablero(entrada, n: int = 9) -> list[list[int]]:
    """
    Convierte una entrada a una matriz n x n.

    Tipos soportados:
    - cadena CSV con números separados por comas
    - ruta a archivo de texto
    - lista plana con n*n elementos
    - matriz n x n
    """
    _tamano_subcuadro(n)
    total = n * n

    if _es_matriz(entrada, n):
        tablero = [list(map(int, fila)) for fila in entrada]
        if not validar_tablero(tablero, n):
            raise ValueError("La matriz suministrada no es un tablero válido.")
        return tablero

    if isinstance(entrada, (list, tuple)):
        valores = _normalizar_valores(entrada, total)
        tablero = [valores[i : i + n] for i in range(0, total, n)]
        if not validar_tablero(tablero, n):
            raise ValueError("La lista plana no genera un tablero válido.")
        return tablero

    if isinstance(entrada, str):
        contenido = entrada
        ruta = Path(entrada)

        if ruta.is_file():
            contenido = ruta.read_text(encoding="utf-8")

        texto = contenido.strip()
        if not texto:
            raise ValueError("La entrada de texto está vacía.")

        if "\n" in texto:
            valores = []
            for linea in texto.splitlines():
                linea = linea.strip()
                if not linea:
                    continue
                partes = [parte.strip() for parte in linea.replace(";", ",").split(",")]
                valores.extend(parte for parte in partes if parte != "")
        else:
            valores = [parte.strip() for parte in texto.replace(";", ",").split(",") if parte.strip() != ""]

        valores_enteros = _normalizar_valores(valores, total)
        tablero = [valores_enteros[i : i + n] for i in range(0, total, n)]
        if not validar_tablero(tablero, n):
            raise ValueError("La entrada de texto no representa un tablero válido.")
        return tablero

    raise TypeError("Tipo de entrada no soportado para leer_tablero.")


def validar_fila(tablero: list[list[int]], fila: int, num: int, n: int) -> bool:
    """Verifica si un número puede estar en una fila sin repetirse."""
    for col in range(n):
        if tablero[fila][col] == num:
            return False
    return True


def validar_columna(tablero: list[list[int]], col: int, num: int, n: int) -> bool:
    """Verifica si un número puede estar en una columna sin repetirse."""
    for fila in range(n):
        if tablero[fila][col] == num:
            return False
    return True


def validar_cuadro(tablero: list[list[int]], fila: int, col: int, num: int, n: int) -> bool:
    """Verifica si un número puede estar en su subcuadro sin repetirse."""
    tam = _tamano_subcuadro(n)
    inicio_fila = (fila // tam) * tam
    inicio_col = (col // tam) * tam

    for i in range(inicio_fila, inicio_fila + tam):
        for j in range(inicio_col, inicio_col + tam):
            if tablero[i][j] == num:
                return False
    return True


def es_posicion_valida(tablero: list[list[int]], fila: int, col: int, num: int, n: int) -> bool:
    """Valida si num puede colocarse en la posición indicada."""
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
    """Verifica dimensiones, rango de valores y consistencia del tablero."""
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
    """Muestra el tablero con separadores entre subcuadros."""
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
    ruta_prueba = "sudoku_prueba.txt"
    tablero = leer_tablero(ruta_prueba)
    print(f"Prueba desde archivo: {ruta_prueba}")
    print("Tablero válido:", validar_tablero(tablero, 9))
    imprimir_tablero(tablero)
