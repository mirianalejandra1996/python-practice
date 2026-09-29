"""
Ejercicios — Archivos CSV

! Ejecuta este script desde la carpeta csv_files/ para que los .csv se creen aquí:
!   cd week7/exercises/csv_files
!   py ejercicios_csv.py
"""

import csv


# ============================================================================================
# Ejercicio 1: Crear y leer un inventario (Fácil)
# Crea inventario.csv con 5 productos (nombre, precio, cantidad).
# Luego léelo con DictReader e imprime cada producto con formato legible.
# ============================================================================================

productos = [
    {"nombre": "Café", "precio": "45.00", "cantidad": "100"},
    {"nombre": "Pan", "precio": "25.50", "cantidad": "200"},
    {"nombre": "Leche", "precio": "32.00", "cantidad": "150"},
    {"nombre": "Galletas", "precio": "18.75", "cantidad": "80"},
    {"nombre": "Jugo", "precio": "28.00", "cantidad": "120"},
]

campos = ["nombre", "precio", "cantidad"]

with open("inventario.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(productos)

print("Inventario:")
with open("inventario.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        nombre = fila["nombre"]
        precio = float(fila["precio"])
        cantidad = int(fila["cantidad"])
        print(f"  {nombre}: ${precio:.2f} ({cantidad} unidades)")


# ============================================================================================
# Ejercicio 2: Filtrar datos de un CSV (Fácil)
# Lee inventario.csv e imprime solo los productos con precio mayor a $25.
# ============================================================================================

print("\nProductos con precio mayor a $25.00:")
print("-" * 40)

with open("inventario.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for fila in reader:
        precio = float(fila["precio"])
        if precio > 25:
            nombre = fila["nombre"]
            cantidad = int(fila["cantidad"])
            print(f"  {nombre}: ${precio:.2f} ({cantidad} unidades)")


# ============================================================================================
# Ejercicio 3: Agregar columna de promedio (Medio)
# 1. Crea notas.csv con columnas: nombre, tarea_1, tarea_2, tarea_3 (al menos 4 estudiantes)
# 2. Lee el CSV
# 3. Calcula el promedio de las 3 tareas para cada estudiante
# 4. Escribe notas_con_promedio.csv con las columnas originales + "promedio"
# 5. Imprime el resultado
# ============================================================================================

notas = [
    {"nombre": "Ana", "tarea_1": 90, "tarea_2": 85, "tarea_3": 95},
    {"nombre": "Carlos", "tarea_1": 70, "tarea_2": 75, "tarea_3": 68},
    {"nombre": "María", "tarea_1": 100, "tarea_2": 92, "tarea_3": 97},
    {"nombre": "Pedro", "tarea_1": 60, "tarea_2": 72, "tarea_3": 65},
]

campos = ["nombre", "tarea_1", "tarea_2", "tarea_3"]

with open("notas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(notas)

con_promedio = []

with open("notas.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        tareas = [int(fila["tarea_1"]), int(fila["tarea_2"]), int(fila["tarea_3"])]
        fila["promedio"] = round(sum(tareas) / len(tareas), 1)
        con_promedio.append(fila)

campos_salida = campos + ["promedio"]

with open("notas_con_promedio.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos_salida)
    writer.writeheader()
    writer.writerows(con_promedio)

print("\nArchivo notas_con_promedio.csv generado:")
for fila in con_promedio:
    print(f"  {fila['nombre']}: {fila['promedio']}")


# ============================================================================================
# Ejercicio 4: Combinar dos CSV (Medio)
# 1. Crea lista_a.csv con 4 contactos
# 2. Crea lista_b.csv con 4 contactos (2 repetidos de lista_a)
# 3. Lee ambos archivos
# 4. Combínalos eliminando duplicados por email
# 5. Escribe combinado.csv
# ============================================================================================

lista_a = [
    {"nombre": "Ana", "email": "ana@mail.com"},
    {"nombre": "Carlos", "email": "carlos@mail.com"},
    {"nombre": "María", "email": "maria@mail.com"},
    {"nombre": "Pedro", "email": "pedro@mail.com"},
]

lista_b = [
    {"nombre": "Lucía", "email": "lucia@mail.com"},
    {"nombre": "Carlos", "email": "carlos@mail.com"},
    {"nombre": "Roberto", "email": "roberto@mail.com"},
    {"nombre": "Ana", "email": "ana@mail.com"},
]

campos = ["nombre", "email"]

for nombre_archivo, datos in [("lista_a.csv", lista_a), ("lista_b.csv", lista_b)]:
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)

emails_vistos = set()
combinados = []

for nombre_archivo in ["lista_a.csv", "lista_b.csv"]:
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila["email"] not in emails_vistos:
                emails_vistos.add(fila["email"])
                combinados.append(fila)

with open("combinado.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(combinados)

print(f"\nLista A: {len(lista_a)} contactos")
print(f"Lista B: {len(lista_b)} contactos")
print(f"Combinado (sin duplicados): {len(combinados)} contactos\n")

with open("combinado.csv", "r", encoding="utf-8") as f:
    print(f.read())
