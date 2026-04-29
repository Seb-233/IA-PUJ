# MiniProyecto 1 - Base de conocimiento

Esta carpeta contiene una base de conocimiento medica para un sistema experto de diagnostico preliminar.
La base esta definida en `base_conocimiento.json` y contiene reglas que relacionan sintomas, hallazgos clinicos, hechos intermedios y posibles diagnosticos.

Cada regla sigue la forma:

```text
antecedentes -> consecuente
```

Los antecedentes son una lista de hechos que deben cumplirse al mismo tiempo, es decir, estan unidos por AND. El consecuente es un unico hecho positivo que el sistema puede agregar a su memoria de trabajo cuando todos los antecedentes se cumplen.

Ejemplo:

```json
{
  "id": "R1",
  "antecedentes": ["Fiebre", "Tos"],
  "consecuente": "Sindrome_Respiratorio"
}
```

Esta estructura esta pensada para ser usada por un motor de inferencia por encadenamiento hacia adelante. El motor parte de sintomas iniciales, revisa que reglas tienen todos sus antecedentes satisfechos y agrega nuevos hechos hasta deducir un objetivo o llegar a un punto fijo.
