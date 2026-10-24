"""
Ejercicios — Compresión con zipfile

! Todo ocurre dentro de la carpeta zona_ejercicios/, que se borra y se vuelve a crear
! en cada ejecución.
"""

import csv
import json
import os
import shutil
import zipfile
from datetime import date
from pathlib import Path

# Nos ubicamos en la carpeta de este script, para que todo se cree aquí
# sin importar desde dónde lo ejecutes
os.chdir(Path(__file__).parent)

ZONA = Path("zona_ejercicios")
if ZONA.exists():
    shutil.rmtree(ZONA)
ZONA.mkdir()


# ============================================================================================
# Ejercicio 1: Crear y explorar un ZIP (Fácil)
# Crea 3 archivos de texto con diferente contenido, agrúpalos en un ZIP, y luego lista
# el contenido del ZIP mostrando el nombre y tamaño de cada archivo.
# ============================================================================================

textos = {
    "saludo.txt": "Hola, mundo\n",
    "lista_compras.txt": "Leche\nPan\nHuevos\nCafé\n",
    "diario.txt": "Hoy aprendí a comprimir archivos con Python.\n" * 20,
}

for nombre, contenido in textos.items():
    (ZONA / nombre).write_text(contenido, encoding="utf-8")

zip_textos = ZONA / "textos.zip"

with zipfile.ZipFile(zip_textos, "w", zipfile.ZIP_DEFLATED) as zf:
    for nombre in textos:
        zf.write(ZONA / nombre, nombre)

print("Ejercicio 1:")
with zipfile.ZipFile(zip_textos, "r") as zf:
    for info in zf.infolist():
        print(f"  {info.filename:<20} {info.file_size:>5} bytes "
              f"(comprimido: {info.compress_size} bytes)")

# Ojo: los archivos muy pequeños quedan un poco MÁS grandes al comprimirlos, porque la
# compresión agrega unos bytes de control. Con texto largo o repetido (diario.txt) sí se
# nota la reducción.


# ============================================================================================
# Ejercicio 2: Backup comprimido con fecha (Medio)
# Crea un script que comprima todos los archivos de un directorio en un ZIP con la fecha
# de hoy en el nombre. Formato: backup_2025-06-15.zip. Muestra un resumen al final.
# ============================================================================================


def backup_directorio(carpeta, destino):
    """Comprime todos los archivos de `carpeta` (incluidas subcarpetas) en un ZIP fechado."""
    carpeta = Path(carpeta)
    destino = Path(destino)

    if not carpeta.is_dir():
        print(f"  Error: '{carpeta}' no es un directorio.")
        return None

    archivos = [a for a in carpeta.rglob("*") if a.is_file()]
    if not archivos:
        print(f"  '{carpeta}' está vacío, no hay nada que respaldar.")
        return None

    destino.mkdir(parents=True, exist_ok=True)
    nombre_zip = destino / f"backup_{date.today().isoformat()}.zip"

    with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for archivo in archivos:
            zf.write(archivo, archivo.relative_to(carpeta))

    tamano_original = sum(a.stat().st_size for a in archivos)
    tamano_zip = nombre_zip.stat().st_size

    print(f"  Backup creado: {nombre_zip.name}")
    print(f"  Archivos:      {len(archivos)}")
    print(f"  Tamaño:        {tamano_original / 1024:.1f} KB → {tamano_zip / 1024:.1f} KB")
    return nombre_zip


# Directorio de prueba con subcarpetas
documentos = ZONA / "documentos"
(documentos / "facturas").mkdir(parents=True)
(documentos / "carta.txt").write_text("Estimado cliente...\n" * 30, encoding="utf-8")
(documentos / "contactos.csv").write_text("nombre,tel\nAna,555-1234\n", encoding="utf-8")
(documentos / "facturas" / "enero.txt").write_text("Total: $1200\n", encoding="utf-8")
(documentos / "facturas" / "febrero.txt").write_text("Total: $950\n", encoding="utf-8")

print("\nEjercicio 2:")
backup = backup_directorio(documentos, ZONA / "backups")

with zipfile.ZipFile(backup, "r") as zf:
    print(f"  Contenido:     {zf.namelist()}")


# ============================================================================================
# Ejercicio 3: Extraer, procesar y resumir (Medio)
# Dado un ZIP que contiene varios archivos CSV, extrae los archivos, cuenta las filas de
# cada CSV, y escribe un archivo resumen.json con los resultados.
# ============================================================================================

# Preparamos el ZIP de entrada con 3 CSVs (y un archivo que no es CSV)
zip_datos = ZONA / "datos.zip"

with zipfile.ZipFile(zip_datos, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("ventas.csv", "producto,cantidad,precio\nLaptop,2,15000\nMouse,10,250\nTeclado,5,800\n")
    zf.writestr("clientes.csv", "nombre,ciudad\nAna,CDMX\nLuis,Lima\n")
    zf.writestr("inventario/almacen.csv", "sku,stock\nA1,40\nB2,0\nC3,15\nD4,7\n")
    zf.writestr("notas.txt", "Este archivo no es CSV y se ignora")

carpeta_extraida = ZONA / "datos_extraidos"

# 1. Extraer
with zipfile.ZipFile(zip_datos, "r") as zf:
    zf.extractall(carpeta_extraida)

# 2. Contar filas de cada CSV (sin contar el encabezado)
resumen = {}
for ruta_csv in sorted(carpeta_extraida.rglob("*.csv")):
    with open(ruta_csv, "r", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    nombre = ruta_csv.relative_to(carpeta_extraida).as_posix()
    resumen[nombre] = len(filas)

resultado = {
    "zip": zip_datos.name,
    "archivos_csv": len(resumen),
    "total_filas": sum(resumen.values()),
    "filas_por_archivo": resumen,
}

# 3. Guardar el resumen
with open(ZONA / "resumen.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("\nEjercicio 3:")
for nombre, filas in resumen.items():
    print(f"  {nombre:<25} {filas} filas")
print(f"  Total: {resultado['total_filas']} filas en {resultado['archivos_csv']} CSVs")
print("  Resumen guardado en resumen.json")
