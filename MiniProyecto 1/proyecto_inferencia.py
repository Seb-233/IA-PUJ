import json

# ==========================================================
# PARTE 1: ESTRUCTURA DE DATOS (NO MODIFICAR)
# ==========================================================
class Regla:
    def __init__(self, id_regla, antecedentes, consecuente):
        self.id_regla = id_regla
        self.antecedentes = set(antecedentes)  
        self.consecuente = consecuente

    def __str__(self):
        return f"{self.id_regla}: {' AND '.join(self.antecedentes)} -> {self.consecuente}"

class MotorInferencia:
    def __init__(self, ruta_kb):
        self.reglas = self.cargar_kb(ruta_kb)
        self.memoria_trabajo = set()

    def cargar_kb(self, ruta):
        """Carga las reglas desde un archivo JSON."""
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return [Regla(r.get('id'), r['antecedentes'], r['consecuente']) for r in datos['reglas']]
        except Exception as e:
            print(f"Error al cargar la Base de Conocimiento: {e}")
            return []

    # ==========================================================
    # PARTE 2: ALGORITMO DE ENCADENAMIENTO HACIA ADELANTE
    # ==========================================================
    def ejecutar_inferencia(self, hechos_iniciales, objetivo):
        """
        AQUÍ DEBEN PROGRAMAR EL ALGORITMO.
        
        Entradas:
        - hechos_iniciales: Lista de síntomas (ej. ["Fiebre", "Tos"])
        - objetivo: El diagnóstico a verificar (ej. "Neumonia")
        
        Retorna:
        - True si el objetivo es consecuencia lógica (KB |= objetivo).
        - False si se alcanza un punto fijo sin hallar el objetivo.
        """
        self.memoria_trabajo = set(hechos_iniciales)
        hubo_cambios = True
        
        # TODO: Implementar el ciclo while que busque el 'Punto Fijo'
        # 1. Iterar mientras 'hubo_cambios' sea True.
        # 2. Dentro, iterar por cada regla en 'self.reglas'.
        # 3. Verificar si los antecedentes de la regla son un SUBCONJUNTO de la memoria_trabajo.
        # 4. Si se cumple y el consecuente es nuevo:
        #    - Agregarlo a memoria_trabajo.
        #    - Marcar que hubo_cambios.
        #    - Verificar si el nuevo hecho es el objetivo para retornar True inmediatamente.
        self.traza = []

        while hubo_cambios:
            hubo_cambios = False
            for regla in self.reglas:
                if (regla.antecedentes.issubset(self.memoria_trabajo)
                        and regla.consecuente not in self.memoria_trabajo):
                    self.memoria_trabajo.add(regla.consecuente)
                    self.traza.append(regla)
                    hubo_cambios = True
                    if regla.consecuente == objetivo:
                        return True

        return False # Cambiar por el resultado lógico

# ==========================================================
# PARTE 3: EJECUCIÓN (PUEDEN MODIFICAR PARA PRUEBAS)
# ==========================================================
if __name__ == "__main__":
    # 1. Inicializar el motor con el archivo de reglas
    motor = MotorInferencia("base_conocimiento.json")

    # 2. Definir caso clínico de prueba
    sintomas = ["Fiebre", "Tos", "Dificultad_Respiratoria"]
    hipotesis = "Neumonia"

    print(f"--- Sistema Experto de Diagnóstico ---")
    print(f"Síntomas iniciales: {sintomas}")
    print(f"Objetivo a verificar: {hipotesis}")

    # 3. Ejecutar Inferencia
    resultado = motor.ejecutar_inferencia(sintomas, hipotesis)

    # 4. Mostrar resultado
    print(f"\n¿Es consecuencia lógica?: {resultado}")

    # 5. Mostrar traza de explicación
    if motor.traza:
        print("\n--- Traza de Explicación ---")
        for i, regla in enumerate(motor.traza, 1):
            print(f"  Paso {i}: {regla}")
    print(f"\nHechos en memoria de trabajo: {motor.memoria_trabajo}")