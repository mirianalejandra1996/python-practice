contenido_articulo = """La inteligencia artificial está transformando la industria del software.
Los modelos de lenguaje pueden generar código, analizar datos y automatizar tareas.
La inteligencia artificial no reemplaza a los programadores, los potencia.
Aprender a programar en la era de la inteligencia artificial es más importante que nunca.
Los programadores que usan inteligencia artificial son más productivos.
"""

with open("articulo.txt", "w") as f:
    f.write(contenido_articulo)

with open("articulo.txt", "r") as f:
    texto = f.read().lower()

for signo in ".,;:!?¿¡()\"'":
    texto = texto.replace(signo, "")

palabras = texto.split()
frecuencia = {}

for palabra in palabras:
    frecuencia[palabra] = frecuencia.get(palabra, 0) + 1

top_5 = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)[:5]

print("Top 5 palabras más frecuentes:")
print("-" * 30)
for palabra, conteo in top_5:
    print(f"  {palabra}: {conteo} veces")