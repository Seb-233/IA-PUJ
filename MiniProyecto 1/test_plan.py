"""
Plan de Pruebas - MiniProyecto 1
Sistema Experto de Diagnostico Medico
"""
import json
from proyecto_inferencia import MotorInferencia

# Contadores globales
total_pruebas = 0
pruebas_aprobadas = 0
pruebas_fallidas = 0


def mostrar_resultado(nombre_prueba, aprobada, detalle=""):
    """Imprime si una prueba paso o fallo."""
    global total_pruebas, pruebas_aprobadas, pruebas_fallidas
    total_pruebas += 1
    if aprobada:
        pruebas_aprobadas += 1
        print(f"  [APROBADA]  {nombre_prueba}")
    else:
        pruebas_fallidas += 1
        print(f"  [FALLIDA]   {nombre_prueba}")
        if detalle:
            print(f"              -> {detalle}")


# ==============================================================
# BLOQUE 1: PRUEBAS ESTRUCTURALES DE LA BASE DE CONOCIMIENTO
# ==============================================================
print("=" * 60)
print("BLOQUE 1: PRUEBAS ESTRUCTURALES DE LA BASE DE CONOCIMIENTO")
print("=" * 60)

# KB-01: Carga correcta del JSON
try:
    with open("base_conocimiento.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    reglas = datos["reglas"]
    mostrar_resultado("KB-01 Carga correcta del JSON", True)
except Exception as e:
    mostrar_resultado("KB-01 Carga correcta del JSON", False, str(e))
    reglas = []

# KB-02: Cantidad minima de reglas (>=50)
cantidad = len(reglas)
mostrar_resultado(
    f"KB-02 Cantidad minima de reglas (se encontraron {cantidad})",
    cantidad >= 50
)

# KB-03: Formato de clausula de Horn
# Cada regla debe tener antecedentes (lista) y un unico consecuente (string)
errores_horn = []
for r in reglas:
    if not isinstance(r.get("antecedentes"), list) or len(r["antecedentes"]) == 0:
        errores_horn.append(r.get("id", "?"))
    if not isinstance(r.get("consecuente"), str) or not r["consecuente"]:
        errores_horn.append(r.get("id", "?"))
    # Revisar que no haya OR ni negaciones
    for a in r.get("antecedentes", []):
        if " OR " in a or a.startswith("NOT ") or a.startswith("!"):
            errores_horn.append(r.get("id", "?"))

mostrar_resultado(
    "KB-03 Formato clausula de Horn",
    len(errores_horn) == 0,
    f"Reglas con problemas: {errores_horn}" if errores_horn else ""
)

# KB-04: Existencia de hechos intermedios
# Un hecho intermedio es aquel que aparece como consecuente Y tambien como antecedente
consecuentes = set()
todos_antecedentes = set()
for r in reglas:
    consecuentes.add(r["consecuente"])
    todos_antecedentes.update(r["antecedentes"])

hechos_intermedios = consecuentes & todos_antecedentes
mostrar_resultado(
    f"KB-04 Existencia de hechos intermedios ({len(hechos_intermedios)} encontrados)",
    len(hechos_intermedios) >= 5
)

# KB-05: Aciclicidad
# Revisamos si algun consecuente vuelve a aparecer como camino hacia si mismo
# Construimos las dependencias entre hechos inferidos
dependencias = {}
for r in reglas:
    c = r["consecuente"]
    if c not in dependencias:
        dependencias[c] = set()
    for a in r["antecedentes"]:
        if a in consecuentes:
            dependencias[c].add(a)

# Recorremos cada hecho y verificamos que no haya un camino circular
hay_ciclo = False
for inicio in dependencias:
    visitados = set()
    pila = [inicio]
    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        for dep in dependencias.get(actual, []):
            if dep == inicio:
                hay_ciclo = True
                break
            pila.append(dep)
        if hay_ciclo:
            break
    if hay_ciclo:
        break

mostrar_resultado("KB-05 Aciclicidad", not hay_ciclo,
                  "Se encontro al menos un ciclo" if hay_ciclo else "")

# KB-06: Alcanzabilidad de reglas
# Usamos todos los sintomas iniciales (hojas) y simulamos inferencia completa
sintomas_hoja = set()
for r in reglas:
    for a in r["antecedentes"]:
        if a not in consecuentes:
            sintomas_hoja.add(a)

memoria = set(sintomas_hoja)
hubo_cambio = True
while hubo_cambio:
    hubo_cambio = False
    for r in reglas:
        if set(r["antecedentes"]).issubset(memoria) and r["consecuente"] not in memoria:
            memoria.add(r["consecuente"])
            hubo_cambio = True

no_alcanzables = consecuentes - memoria
mostrar_resultado(
    "KB-06 Alcanzabilidad de reglas",
    len(no_alcanzables) == 0,
    f"Reglas no alcanzables: {no_alcanzables}" if no_alcanzables else ""
)

# KB-07: Consistencia de nombres
# Verificar que no haya variaciones como "Vomito" vs "Vomitos"
todos_los_hechos = sorted(todos_antecedentes | consecuentes)
problemas_nombre = []
for i, a in enumerate(todos_los_hechos):
    for b in todos_los_hechos[i+1:]:
        if a.lower() == b.lower() and a != b:
            problemas_nombre.append(f"'{a}' vs '{b}'")
    if " " in a:
        problemas_nombre.append(f"Espacio en '{a}'")

mostrar_resultado(
    "KB-07 Consistencia de nombres",
    len(problemas_nombre) == 0,
    f"Problemas: {problemas_nombre}" if problemas_nombre else ""
)


# ==============================================================
# BLOQUE 2: PRUEBAS FUNCIONALES - CASOS POSITIVOS
# ==============================================================
print("\n" + "=" * 60)
print("BLOQUE 2: PRUEBAS FUNCIONALES - CASOS POSITIVOS")
print("=" * 60)

motor = MotorInferencia("base_conocimiento.json")


def probar_caso_positivo(nombre, sintomas, objetivo, reglas_esperadas, hechos_esperados):
    """Ejecuta un caso donde se espera que el motor retorne True."""
    resultado = motor.ejecutar_inferencia(sintomas, objetivo)
    traza_ids = [r.id_regla for r in motor.traza]
    
    # Verificar resultado, reglas en traza y hechos inferidos
    resultado_correcto = resultado == True
    reglas_encontradas = all(r in traza_ids for r in reglas_esperadas)
    hechos_encontrados = all(h in motor.memoria_trabajo for h in hechos_esperados)
    
    aprobada = resultado_correcto and reglas_encontradas and hechos_encontrados
    
    detalle = ""
    if not resultado_correcto:
        detalle += f"Resultado={resultado} (esperado True). "
    if not reglas_encontradas:
        faltantes = [r for r in reglas_esperadas if r not in traza_ids]
        detalle += f"Reglas faltantes: {faltantes}. "
    if not hechos_encontrados:
        faltantes = [h for h in hechos_esperados if h not in motor.memoria_trabajo]
        detalle += f"Hechos faltantes: {faltantes}. "
    
    mostrar_resultado(nombre, aprobada, detalle)
    
    # Imprimir evidencia
    print(f"              Sintomas: {sintomas}")
    print(f"              Objetivo: {objetivo}")
    print(f"              Resultado: {resultado}")
    print(f"              Traza: {traza_ids}")
    print(f"              Hechos inferidos: {sorted(motor.memoria_trabajo - set(sintomas))}")


# FC-01: Neumonia
probar_caso_positivo("FC-01 Neumonia",
    ["Fiebre", "Tos", "Dificultad_Respiratoria"], "Neumonia",
    ["R1", "R2"], ["Infeccion_Respiratoria", "Neumonia"])

# FC-02: Influenza
probar_caso_positivo("FC-02 Influenza",
    ["Dolor_Muscular", "Fiebre", "Escalofrios"], "Influenza",
    ["R3", "R5"], ["Gripe", "Influenza"])

# FC-03: COVID severo
probar_caso_positivo("FC-03 COVID severo",
    ["Perdida_Olfato", "Perdida_Gusto", "Fiebre", "Tos", "Dificultad_Respiratoria"],
    "COVID_Severo",
    ["R6", "R7", "R8", "R9"],
    ["Disfuncion_Quimiosensorial", "Sospecha_COVID", "COVID_Probable", "COVID_Severo"])

# FC-04: Tuberculosis activa
probar_caso_positivo("FC-04 Tuberculosis activa",
    ["Tos_Con_Sangre", "Perdida_Peso", "Sudoracion_Nocturna", "Fiebre"],
    "Tuberculosis_Activa",
    ["R10", "R11", "R12"],
    ["Sospecha_TBC", "Tuberculosis", "Tuberculosis_Activa"])

# FC-05: Crisis asmatica
probar_caso_positivo("FC-05 Crisis asmatica",
    ["Sibilancias", "Opresion_Pecho", "Dificultad_Respiratoria", "Tos"],
    "Crisis_Asmatica",
    ["R16", "R17", "R18"],
    ["Obstruccion_Via_Aerea", "Asma_Aguda", "Crisis_Asmatica"])

# FC-06: Infarto de miocardio
probar_caso_positivo("FC-06 Infarto de miocardio",
    ["Dolor_Pecho", "Sudoracion_Fria", "Dolor_Brazo_Izquierdo", "Palpitaciones"],
    "Infarto_Miocardio",
    ["R19", "R20", "R21"],
    ["Sospecha_Cardiaca", "Sindrome_Coronario_Agudo", "Infarto_Miocardio"])

# FC-07: Insuficiencia cardiaca
probar_caso_positivo("FC-07 Insuficiencia cardiaca",
    ["Palpitaciones", "Fatiga", "Opresion_Pecho", "Mareo"],
    "Insuficiencia_Cardiaca",
    ["R22", "R23", "R24"],
    ["Disfuncion_Cardiaca", "Angina_Pecho", "Insuficiencia_Cardiaca"])

# FC-08: Apendicitis complicada
probar_caso_positivo("FC-08 Apendicitis complicada",
    ["Dolor_Abdominal", "Nauseas", "Vomitos", "Dolor_Fosa_Iliaca_Derecha", "Fiebre"],
    "Apendicitis_Complicada",
    ["R25", "R26", "R27", "R28"],
    ["Sindrome_Digestivo", "Sindrome_Abdominal_Agudo", "Apendicitis", "Apendicitis_Complicada"])

# FC-09: Gastroenteritis infecciosa
probar_caso_positivo("FC-09 Gastroenteritis infecciosa",
    ["Diarrea", "Vomitos", "Dolor_Abdominal", "Fiebre"],
    "Gastroenteritis_Infecciosa",
    ["R29", "R30", "R31"],
    ["Trastorno_Gastrointestinal", "Gastroenteritis", "Gastroenteritis_Infecciosa"])

# FC-10: Diabetes tipo 2
probar_caso_positivo("FC-10 Diabetes tipo 2",
    ["Sed_Excesiva", "Miccion_Frecuente", "Fatiga", "Vision_Borrosa"],
    "Diabetes_Tipo2",
    ["R32", "R33", "R34"],
    ["Poliuria_Polidipsia", "Hiperglucemia_Cronica", "Diabetes_Tipo2"])

# FC-11: Hipertension severa
probar_caso_positivo("FC-11 Hipertension severa",
    ["Dolor_Cabeza", "Mareo", "Presion_Alta", "Taquicardia"],
    "Hipertension_Severa",
    ["R36", "R37", "R38"],
    ["Sintomas_Vasculares", "Hipertension_Arterial", "Hipertension_Severa"])

# FC-12: Dengue con signos de alarma
probar_caso_positivo("FC-12 Dengue con signos de alarma",
    ["Fiebre", "Dolor_Detras_Ojos", "Dolor_Muscular", "Erupcion_Cutanea", "Vomitos"],
    "Dengue_Con_Signos_Alarma",
    ["R40", "R41", "R42", "R43"],
    ["Fiebre_Retro_Ocular", "Sospecha_Dengue", "Dengue_Clasico", "Dengue_Con_Signos_Alarma"])

# FC-13: Malaria
probar_caso_positivo("FC-13 Malaria",
    ["Anemia", "Fatiga", "Fiebre", "Escalofrios"],
    "Malaria",
    ["R44", "R45", "R46"],
    ["Sindrome_Anemico", "Fiebre_Hemolitica", "Malaria"])

# FC-14: Meningitis
probar_caso_positivo("FC-14 Meningitis",
    ["Fiebre", "Rigidez_Cuello", "Dolor_Cabeza", "Fotofobia", "Confusion_Mental"],
    "Meningitis",
    ["R47", "R48", "R49", "R50"],
    ["Irritacion_Meningea", "Cefalea_Meningea", "Sospecha_Meningitis", "Meningitis"])

# FC-15: Insuficiencia renal
probar_caso_positivo("FC-15 Insuficiencia renal",
    ["Orina_Oscura", "Dolor_Lumbar", "Fatiga", "Nauseas"],
    "Insuficiencia_Renal",
    ["R51", "R52", "R53"],
    ["Disfuncion_Renal", "Falla_Renal_Incipiente", "Insuficiencia_Renal"])

# FC-16: Sepsis severa
probar_caso_positivo("FC-16 Sepsis severa",
    ["Fiebre", "Tos", "Taquicardia", "Confusion_Mental"],
    "Sepsis_Severa",
    ["R1", "R54", "R55", "R56"],
    ["Infeccion_Respiratoria", "Respuesta_Inflamatoria_Sistemica", "Sepsis_Temprana", "Sepsis_Severa"])


# ==============================================================
# BLOQUE 3: PRUEBAS NEGATIVAS
# ==============================================================
print("\n" + "=" * 60)
print("BLOQUE 3: PRUEBAS NEGATIVAS")
print("=" * 60)


def probar_caso_negativo(nombre, sintomas, objetivo, hechos_si_esperados, hechos_no_esperados):
    """Ejecuta un caso donde se espera que el motor retorne False."""
    resultado = motor.ejecutar_inferencia(sintomas, objetivo)
    traza_ids = [r.id_regla for r in motor.traza]
    
    resultado_correcto = resultado == False
    hechos_si_encontrados = all(h in motor.memoria_trabajo for h in hechos_si_esperados)
    hechos_no_presentes = all(h not in motor.memoria_trabajo for h in hechos_no_esperados)
    
    aprobada = resultado_correcto and hechos_si_encontrados and hechos_no_presentes
    
    detalle = ""
    if not resultado_correcto:
        detalle += f"Resultado={resultado} (esperado False). "
    if not hechos_si_encontrados:
        detalle += f"Hechos que deberian estar: {[h for h in hechos_si_esperados if h not in motor.memoria_trabajo]}. "
    if not hechos_no_presentes:
        detalle += f"Hechos que NO deberian estar: {[h for h in hechos_no_esperados if h in motor.memoria_trabajo]}. "
    
    mostrar_resultado(nombre, aprobada, detalle)
    
    print(f"              Sintomas: {sintomas}")
    print(f"              Objetivo: {objetivo}")
    print(f"              Resultado: {resultado}")
    print(f"              Traza: {traza_ids}")
    print(f"              Memoria: {sorted(motor.memoria_trabajo)}")


# FN-01: Neumonia incompleta (falta Dificultad_Respiratoria)
probar_caso_negativo("FN-01 Neumonia incompleta",
    ["Fiebre", "Tos"], "Neumonia",
    ["Infeccion_Respiratoria"], ["Neumonia"])

# FN-02: COVID severo incompleto (falta Dificultad_Respiratoria)
probar_caso_negativo("FN-02 COVID severo incompleto",
    ["Perdida_Olfato", "Perdida_Gusto", "Fiebre", "Tos"], "COVID_Severo",
    ["Disfuncion_Quimiosensorial", "Sospecha_COVID", "COVID_Probable"], ["COVID_Severo"])

# FN-03: Tuberculosis sin sudoracion nocturna
probar_caso_negativo("FN-03 Tuberculosis sin sudoracion",
    ["Tos_Con_Sangre", "Perdida_Peso"], "Tuberculosis",
    ["Sospecha_TBC"], ["Tuberculosis"])

# FN-04: Apendicitis sin dolor especifico
probar_caso_negativo("FN-04 Apendicitis sin dolor especifico",
    ["Dolor_Abdominal", "Nauseas", "Vomitos"], "Apendicitis",
    ["Sindrome_Digestivo", "Sindrome_Abdominal_Agudo"], ["Apendicitis"])

# FN-05: Objetivo de otra rama (sintomas vasculares, objetivo respiratorio)
probar_caso_negativo("FN-05 Objetivo de otra rama",
    ["Dolor_Cabeza", "Mareo", "Presion_Alta"], "Neumonia",
    ["Sintomas_Vasculares", "Hipertension_Arterial"], ["Neumonia"])

# FN-06: Sintomas que no existen en la KB
probar_caso_negativo("FN-06 Sintomas no registrados",
    ["Sintoma_No_Registrado_1", "Sintoma_No_Registrado_2"], "Neumonia",
    [], ["Neumonia"])


# ==============================================================
# BLOQUE 4: PRUEBAS DE PUNTO FIJO
# ==============================================================
print("\n" + "=" * 60)
print("BLOQUE 4: PRUEBAS DE PUNTO FIJO")
print("=" * 60)


def probar_punto_fijo(nombre, sintomas, objetivo, hechos_esperados):
    """Verifica que el motor se detenga correctamente en punto fijo."""
    resultado = motor.ejecutar_inferencia(sintomas, objetivo)
    traza_ids = [r.id_regla for r in motor.traza]
    inferidos = motor.memoria_trabajo - set(sintomas)
    
    resultado_correcto = resultado == False
    
    if hechos_esperados:
        hechos_correctos = set(hechos_esperados) == inferidos
    else:
        hechos_correctos = len(inferidos) == 0
    
    aprobada = resultado_correcto and hechos_correctos
    
    detalle = ""
    if not resultado_correcto:
        detalle += f"Resultado={resultado} (esperado False). "
    if not hechos_correctos:
        detalle += f"Inferidos={sorted(inferidos)} vs esperados={hechos_esperados}. "
    
    mostrar_resultado(nombre, aprobada, detalle)
    
    print(f"              Sintomas: {sintomas}")
    print(f"              Objetivo: {objetivo}")
    print(f"              Resultado: {resultado}")
    print(f"              Inferidos: {sorted(inferidos)}")
    print(f"              Traza: {traza_ids}")


# PF-01: Punto fijo con inferencia parcial
probar_punto_fijo("PF-01 Punto fijo con inferencia parcial",
    ["Fiebre", "Tos"], "COVID_Severo",
    ["Infeccion_Respiratoria"])

# PF-02: Punto fijo sin ninguna inferencia
probar_punto_fijo("PF-02 Punto fijo sin inferencia",
    ["Dolor_Inexistente", "Sintoma_X"], "Meningitis",
    [])


# ==============================================================
# BLOQUE 5: PRUEBAS DE TRAZA DE EXPLICACION
# ==============================================================
print("\n" + "=" * 60)
print("BLOQUE 5: PRUEBAS DE TRAZA DE EXPLICACION")
print("=" * 60)

# TR-01: Traza corta (Neumonia)
motor.ejecutar_inferencia(["Fiebre", "Tos", "Dificultad_Respiratoria"], "Neumonia")
traza_01 = [r.id_regla for r in motor.traza]
mostrar_resultado("TR-01 Traza corta (Neumonia)", traza_01 == ["R1", "R2"])
print(f"              Traza esperada: ['R1', 'R2']")
print(f"              Traza obtenida: {traza_01}")

# TR-02: Traza larga (COVID severo)
motor.ejecutar_inferencia(
    ["Perdida_Olfato", "Perdida_Gusto", "Fiebre", "Tos", "Dificultad_Respiratoria"],
    "COVID_Severo")
traza_02 = [r.id_regla for r in motor.traza]
tiene_reglas_covid = all(r in traza_02 for r in ["R6", "R7", "R8", "R9"])
mostrar_resultado("TR-02 Traza larga (COVID severo)", tiene_reglas_covid)
print(f"              Debe incluir: R6, R7, R8, R9")
print(f"              Traza obtenida: {traza_02}")

# TR-03: Traza con varias ramas activas (Sepsis)
resultado_tr03 = motor.ejecutar_inferencia(
    ["Fiebre", "Tos", "Mucosidad_Excesiva", "Taquicardia", "Confusion_Mental"],
    "Sepsis_Severa")
traza_03 = [r.id_regla for r in motor.traza]
tiene_reglas_sepsis = all(r in traza_03 for r in ["R1", "R54", "R55", "R56"])
mostrar_resultado("TR-03 Traza con varias ramas (Sepsis)",
                  resultado_tr03 == True and tiene_reglas_sepsis)
print(f"              Resultado: {resultado_tr03}")
print(f"              Debe incluir: R1, R54, R55, R56")
print(f"              Traza obtenida: {traza_03}")


# ==============================================================
# BLOQUE 6: PRUEBA DE NO DUPLICACION DE HECHOS
# ==============================================================
print("\n" + "=" * 60)
print("BLOQUE 6: PRUEBA DE NO DUPLICACION DE HECHOS")
print("=" * 60)

motor.ejecutar_inferencia(["Fiebre", "Tos", "Mucosidad_Excesiva"], "Bronquitis_Bacteriana")
memoria_lista = list(motor.memoria_trabajo)
hay_duplicados = len(memoria_lista) != len(set(memoria_lista))
es_conjunto = isinstance(motor.memoria_trabajo, set)

mostrar_resultado("ND-01 No duplicar hechos inferidos",
                  not hay_duplicados and es_conjunto)
print(f"              Memoria es tipo set: {es_conjunto}")
print(f"              Hechos en memoria: {sorted(motor.memoria_trabajo)}")


# ==============================================================
# RESUMEN FINAL
# ==============================================================
print("\n" + "=" * 60)
print("RESUMEN FINAL")
print("=" * 60)
print(f"  Total de pruebas:    {total_pruebas}")
print(f"  Pruebas aprobadas:   {pruebas_aprobadas}")
print(f"  Pruebas fallidas:    {pruebas_fallidas}")

if pruebas_fallidas > 0:
    print("\n  ATENCION: Hay pruebas que fallaron. Revisar los detalles arriba.")
else:
    print("\n  Todas las pruebas pasaron correctamente.")
