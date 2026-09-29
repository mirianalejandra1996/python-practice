texto = """Python es un lenguaje de programación versátil.
Python se usa en ciencia de datos, web, automatización y más.
Aprender Python es una excelente inversión de tiempo.
"""

with open("texto.txt", "w") as f:
    f.write(texto)

with open("texto.txt", "r") as f:
    contenido = f.read()
    palabras = contenido.split()
    print(f"Total de palabras: {len(palabras)}")

    frecuencia = {}
    for palabra in palabras:
        palabra = palabra.lower().strip(".,;:!?")
        frecuencia[palabra] = frecuencia.get(palabra, 0) + 1

    top_5 = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 palabras más frecuentes:")
    for palabra, conteo in top_5:
        print(f"  {palabra}: {conteo}")