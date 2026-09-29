
"""
Ejemplo práctico: procesar un archivo de notas
Vamos a crear un programa completo. Primero creamos el archivo de datos, luego lo procesamos.
"""

# Paso 1: Crear el archivo de datos

datos = [
    "Ana,95,88,92\n",
    "Carlos,78,85,80\n",
    "María,92,96,94\n",
    "Pedro,65,70,72\n",
    "Lucía,88,91,85\n",
]

with open("calificaciones.txt", "w") as f:
    f.writelines(datos)

print("Archivo calificaciones.txt creado.")

# Paso 2: Leer, procesar y escribir resultados

with open("calificaciones.txt", "r") as entrada:
    with open("promedios.txt", "w") as salida:
        salida.write("Nombre,Promedio\n")

        for linea in entrada:
            partes = linea.strip().split(",")
            nombre = partes[0]
            notas = [int(n) for n in partes[1:]]
            promedio = sum(notas) / len(notas)
            salida.write(f"{nombre},{promedio:.1f}\n")

print("Archivo promedios.txt generado.")

with open("promedios.txt", "r") as f:
    print(f.read())
    
    
"""
Este patrón — leer archivo → procesar datos → escribir archivo nuevo — es uno de
los más comunes en programación. Lo vas a usar constantemente.
"""