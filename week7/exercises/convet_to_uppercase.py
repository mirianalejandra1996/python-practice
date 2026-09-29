"""
Ejercicio 3: Convertir a mayúsculas (Medio)
Lee un archivo de texto, convierte todo su contenido a mayúsculas y escríbelo en un archivo nuevo llamado mayusculas.txt.

Pasos:

Crea original.txt con al menos 4 líneas de texto
Lee original.txt
Convierte cada línea a mayúsculas
Escribe el resultado en mayusculas.txt
Lee mayusculas.txt para verificar
"""

with open("original.txt", "w") as f:
    f.write("hola mundo\n")
    f.write("python es genial\n")
    f.write("archivos de texto\n")
    f.write("semana siete del bootcamp\n")

with open("original.txt", "r") as entrada:
    with open("mayusculas.txt", "w") as salida:
        for linea in entrada:
            salida.write(linea.upper())

with open("mayusculas.txt", "r") as f:
    print(f.read())