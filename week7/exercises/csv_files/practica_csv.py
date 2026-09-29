"""
Semana 7: Archivos y Formatos de Datos
Archivos CSV

CSV (Comma-Separated Values) es el formato estándar para datos tabulares.
Lo puedes abrir en Excel, Google Sheets, cualquier editor de texto, y procesarlo con Python.
Python incluye el módulo csv en su librería estándar — no necesitas instalar nada.

! Ejecuta este script desde la carpeta csv_files/ para que los .csv se creen aquí:
!   cd week7/exercises/csv_files
!   py practica_csv.py
"""


# ============================================================================================

"""
¿Qué es CSV?
Un archivo CSV es texto plano donde:
- Cada línea es una fila de datos
- Los valores de cada fila están separados por comas
- La primera línea (opcional pero común) son los encabezados

Ejemplo — un archivo productos.csv:

nombre,precio,cantidad
Café,45.00,100
Pan,25.50,200
Leche,32.00,150
Galletas,18.75,80


¿Por qué CSV y no Excel?

Característica          CSV                         Excel (.xlsx)
Formato                 Texto plano                 Binario
Tamaño                  Pequeño                     Grande
Abrirlo                 Cualquier editor            Necesitas Excel/Sheets
Procesarlo con Python   Módulo csv (built-in)       Necesitas openpyxl (externo)
Portabilidad            Universal                   Depende del software
"""

# Creamos productos.csv para poder usarlo en los ejemplos de lectura
from pathlib import Path

Path("productos.csv").write_text(
    "nombre,precio,cantidad\n"
    "Café,45.00,100\n"
    "Pan,25.50,200\n"
    "Leche,32.00,150\n"
    "Galletas,18.75,80\n",
    encoding="utf-8",
)


# ============================================================================================

"""
Módulo csv: lectura básica
csv.reader — leer filas como listas
"""

import csv

with open("productos.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)

    for fila in reader:
        print(fila)

# ['nombre', 'precio', 'cantidad']
# ['Café', '45.00', '100']
# ...
# Cada fila es una lista de strings. Incluso los números son strings —
# tendrás que convertirlos con int() o float().



# Separar encabezados de datos con next()

with open("productos.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    encabezados = next(reader)

    print(f"Columnas: {encabezados}")
    print()

    for fila in reader:
        nombre = fila[0]
        precio = float(fila[1])
        cantidad = int(fila[2])
        print(f"{nombre}: ${precio:.2f} x {cantidad} unidades")

# next(reader) avanza el reader una fila — consume el encabezado
# para que el for empiece desde los datos.


# ============================================================================================

"""
Módulo csv: escritura básica
csv.writer — escribir filas como listas
"""

with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["nombre", "edad", "ciudad"])
    writer.writerow(["Ana", 25, "CDMX"])
    writer.writerow(["Carlos", 30, "Monterrey"])
    writer.writerow(["María", 28, "Guadalajara"])

print("Archivo salida.csv creado.")

"""
! newline="" — parámetro crítico
! Sin él, en Windows se agregan líneas en blanco extra entre cada fila.
! Regla: siempre incluye newline="" al escribir archivos CSV.
"""



# Escribir múltiples filas con writerows()

datos = [
    ["nombre", "edad", "ciudad"],
    ["Ana", 25, "CDMX"],
    ["Carlos", 30, "Monterrey"],
    ["María", 28, "Guadalajara"],
]

with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(datos)

# writerows() escribe todas las filas de una lista de listas.


# ============================================================================================

"""
DictReader y DictWriter: la forma preferida
Acceder a datos por índice (fila[0], fila[1]) es frágil. Si alguien agrega una
columna al CSV, todos los índices se desplazan y tu código se rompe.
DictReader y DictWriter usan los encabezados como claves de diccionario.
"""

# csv.DictReader — cada fila es un diccionario

with open("productos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for fila in reader:
        print(fila)

# {'nombre': 'Café', 'precio': '45.00', 'cantidad': '100'}
# ...



# Acceder a los valores por nombre

with open("productos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for fila in reader:
        nombre = fila["nombre"]
        precio = float(fila["precio"])
        cantidad = int(fila["cantidad"])
        valor_total = precio * cantidad
        print(f"{nombre}: valor en inventario = ${valor_total:,.2f}")



# csv.DictWriter — escribir diccionarios como filas

estudiantes = [
    {"nombre": "Ana", "matematicas": 95, "ciencias": 88},
    {"nombre": "Carlos", "matematicas": 78, "ciencias": 85},
    {"nombre": "María", "matematicas": 92, "ciencias": 96},
]

campos = ["nombre", "matematicas", "ciencias"]

with open("estudiantes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(estudiantes)

print("Archivo estudiantes.csv creado.")

"""
fieldnames    → define el orden de las columnas
writeheader() → escribe la fila de encabezados
writerows()   → escribe todos los diccionarios como filas

! DictReader y DictWriter son la forma preferida. Úsalos por defecto.
"""


# ============================================================================================

"""
Ejemplo práctico: procesar calificaciones
Flujo completo: datos → lectura → procesamiento → escritura
"""

# Paso 1: Crear el archivo de datos

calificaciones = [
    {"nombre": "Ana", "parcial_1": 95, "parcial_2": 88, "parcial_3": 92},
    {"nombre": "Carlos", "parcial_1": 78, "parcial_2": 85, "parcial_3": 80},
    {"nombre": "María", "parcial_1": 92, "parcial_2": 96, "parcial_3": 94},
    {"nombre": "Pedro", "parcial_1": 65, "parcial_2": 70, "parcial_3": 72},
    {"nombre": "Lucía", "parcial_1": 88, "parcial_2": 91, "parcial_3": 85},
]

campos = ["nombre", "parcial_1", "parcial_2", "parcial_3"]

with open("calificaciones.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(calificaciones)

print("Archivo calificaciones.csv creado.")



# Paso 2: Leer, calcular promedios y escribir resultados

resultados = []

with open("calificaciones.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for fila in reader:
        nombre = fila["nombre"]
        parciales = [
            int(fila["parcial_1"]),
            int(fila["parcial_2"]),
            int(fila["parcial_3"]),
        ]
        promedio = sum(parciales) / len(parciales)
        estado = "Aprobado" if promedio >= 70 else "Reprobado"

        resultados.append({
            "nombre": nombre,
            "parcial_1": parciales[0],
            "parcial_2": parciales[1],
            "parcial_3": parciales[2],
            "promedio": round(promedio, 1),
            "estado": estado,
        })

campos_salida = ["nombre", "parcial_1", "parcial_2", "parcial_3", "promedio", "estado"]

with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos_salida)
    writer.writeheader()
    writer.writerows(resultados)

print("Archivo resultados.csv generado.\n")

for r in resultados:
    print(f"{r['nombre']}: {r['promedio']} → {r['estado']}")

# Este es un patrón que vas a usar constantemente:
# leer CSV → procesar → escribir CSV con resultados.


# ============================================================================================
# TROUBLESHOOTING
# ============================================================================================

# Problema 1: Líneas en blanco extra en Windows

# with open("datos.csv", "w") as f:        # ← falta newline=""
#     writer = csv.writer(f)
#     writer.writerow(["a", "b"])
#     writer.writerow(["1", "2"])

# Causa: el módulo csv agrega \r\n y open() en Windows agrega otro \r. Resultado: \r\r\n.
# Solución: siempre usa newline="" al abrir para escritura:

with open("datos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["a", "b"])
    writer.writerow(["1", "2"])



# Problema 2: Caracteres especiales aparecen corruptos

# with open("datos.csv", "w", newline="") as f:   # ← falta encoding
#     writer = csv.writer(f)
#     writer.writerow(["nombre", "ciudad"])
#     writer.writerow(["José", "São Paulo"])

# Causa: no especificaste el encoding. Python usa el del sistema, que puede no ser UTF-8.
# Solución: siempre incluye encoding="utf-8" al escribir y al leer:

with open("datos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["nombre", "ciudad"])
    writer.writerow(["José", "São Paulo"])

with open("datos.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for fila in reader:
        print(fila)



# Problema 3: Los números se leen como strings

with open("productos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        print(type(fila["precio"]))  # <class 'str'>
        print(fila["precio"] * 2)    # "45.0045.00" — ¡repite el string!
        break

# Causa: el módulo csv lee todo como strings. No hay detección automática de tipos.
# Solución: convierte explícitamente al tipo que necesitas:

with open("productos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        precio = float(fila["precio"])
        cantidad = int(fila["cantidad"])
        total = precio * cantidad
        print(f"Total: ${total:.2f}")

"""
Funciones de conversión comunes:
int(valor)   → entero
float(valor) → decimal
bool(valor)  → ¡cuidado! bool("False") es True (el string no está vacío)
"""


"""
Resumen
- CSV es el formato estándar para datos tabulares — filas y columnas en texto plano
- csv.reader lee filas como listas, csv.writer escribe listas como filas
- csv.DictReader lee filas como diccionarios, csv.DictWriter escribe diccionarios como filas
- Usa DictReader/DictWriter por defecto — acceder por nombre de columna es más robusto
- next(reader) consume la primera fila (útil para separar encabezados)
- Siempre usa newline="" al escribir y encoding="utf-8" en ambas direcciones
- Todos los valores se leen como strings — convierte con int(), float() según necesites
- El patrón leer CSV → procesar → escribir CSV es uno de los más comunes en programación

Recursos adicionales
- Python Docs — csv: https://docs.python.org/3/library/csv.html
- Real Python — Reading and Writing CSV Files: https://realpython.com/python-csv/
- Python Docs — DictReader: https://docs.python.org/3/library/csv.html#csv.DictReader
- CSV Lint (validar archivos CSV): https://csvlint.io/
"""
