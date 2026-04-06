"""Menu simple para cargar y resolver un Sudoku."""

from __future__ import annotations

import time
from copy import deepcopy

from backtracking_basico import solve_sudoku_bt
from backtracking_comprobacion import solve_sudoku_fc
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
            tablero = leer_tablero("Proyecto2/sudoku_prueba.txt")
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
        print("3. Backtracking con comprobación hacia delante (Forward Checking)")
        print("4. Cargar otro tablero")
        print("5. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            tablero = deepcopy(tablero_original)
            print("\nResolviendo con fuerza bruta...\n")
            inicio = time.time()
            res = solve_sudoku_fb(tablero, len(tablero))
            fin = time.time()
            if res:
                print("SOLUCIÓN:")
                imprimir_tablero(tablero)
            else:
                print("Sin solución.")
            print(f"-> Tiempo de ejecución: {fin - inicio:.6f} segundos")
        elif opcion == "2":
            tablero = deepcopy(tablero_original)
            print("\nResolviendo con backtracking basico...\n")
            inicio = time.time()
            res = solve_sudoku_bt(tablero, len(tablero))
            fin = time.time()
            if res:
                print("SOLUCION:")
                imprimir_tablero(tablero)
            else:
                print("Sin solucion.")
            print(f"-> Tiempo de ejecución: {fin - inicio:.6f} segundos")
        elif opcion == "3":
            tablero = deepcopy(tablero_original)
            
            res_pasos = input("¿Desea generar un archivo TXT con el detalle paso a paso de la resolución? (s/n): ").strip().lower()
            generar_txt = res_pasos == 's'
            
            if generar_txt:
                archivo_nombre = "detalles_paso_a_paso.txt"
                print(f"\nResolviendo y documentando el rastro detallado en '{archivo_nombre}'...")
                with open(archivo_nombre, "w", encoding="utf-8") as f:
                    inicio = time.time()
                    res = solve_sudoku_fc(tablero, len(tablero), log_file=f)
                    fin = time.time()
                print(f"El rastro ha sido guardado exitosamente en '{archivo_nombre}'.")
            else:
                print("\nResolviendo con backtracking y forward checking...\n")
                inicio = time.time()
                res = solve_sudoku_fc(tablero, len(tablero))
                fin = time.time()
                
            if res:
                print("\nSOLUCION:")
                imprimir_tablero(tablero)
            else:
                print("\nSin solucion.")
            print(f"-> Tiempo de ejecución: {fin - inicio:.6f} segundos")
        elif opcion == "4":
            tablero_original = cargar_tablero()
        elif opcion == "5":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu_solucion()
