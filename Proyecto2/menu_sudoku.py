"""Menu simple para cargar y resolver un Sudoku."""

from __future__ import annotations

from copy import deepcopy

from backtracking_basico import solve_sudoku_bt
from fuerza_bruta import solve_sudoku_fb
from lectura_sudoku import imprimir_tablero, leer_tablero, validar_tablero


def cargar_tablero() -> list[list[int]]:
    """Permite elegir cómo cargar un tablero."""
    while True:
        print("\nSeleccione el origen del Sudoku:")
        print("1. Archivo de prueba (sudoku_prueba.txt)")
        print("2. Ingresar ruta de archivo manualmente")
        print("3. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            tablero = leer_tablero("sudoku_prueba.txt")
        elif opcion == "2":
            ruta = input("Ruta del archivo: ").strip()
            tablero = leer_tablero(ruta)
        elif opcion == "3":
            raise SystemExit("Programa finalizado por el usuario.")
        else:
            print("Opción no válida. Intente de nuevo.")
            continue

        if not validar_tablero(tablero, len(tablero)):
            print("El tablero cargado no es válido.")
            continue

        return tablero


def menu_solucion() -> None:
    """Muestra el menú principal y ejecuta el método de solución elegido."""
    tablero_original = cargar_tablero()

    while True:
        print("\nTablero cargado:")
        imprimir_tablero(tablero_original)

        print("\nSeleccione la solución que prefiera:")
        print("1. Fuerza bruta")
        print("2. Backtracking basico")
        print("3. Cargar otro tablero")
        print("4. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            tablero = deepcopy(tablero_original)
            print("\nResolviendo con fuerza bruta...\n")
            if solve_sudoku_fb(tablero, len(tablero)):
                print("SOLUCIÓN:")
                imprimir_tablero(tablero)
            else:
                print("Sin solución.")
        elif opcion == "2":
            tablero = deepcopy(tablero_original)
            print("\nResolviendo con backtracking basico...\n")
            if solve_sudoku_bt(tablero, len(tablero)):
                print("SOLUCION:")
                imprimir_tablero(tablero)
            else:
                print("Sin solucion.")
        elif opcion == "3":
            tablero_original = cargar_tablero()
        elif opcion == "4":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu_solucion()
