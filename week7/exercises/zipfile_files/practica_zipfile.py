"""
Semana 7: Archivos y Formatos de Datos
Compresión con zipfile

Los archivos ZIP son el formato de compresión más universal: sirven para enviar varios
archivos por email, descargar datasets, entregar proyectos y hacer backups compactos.

Python incluye el módulo zipfile en su biblioteca estándar — no hay que instalar nada.

¿Por qué comprimir?
Razón               Ejemplo
Reducir tamaño      Un archivo de texto de 10 MB puede quedar en 2 MB
Agrupar archivos    Enviar 50 archivos como un solo .zip
Transporte          Adjuntar en email, compartir por WhatsApp
Backups             Un backup comprimido ocupa menos espacio
Distribución        Descargar datasets, librerías, proyectos

! Todo ocurre dentro de la carpeta zona_practica/, que se borra y se vuelve a crear
! en cada ejecución.
"""

import csv
import json
import os
import shutil
import zipfile
from datetime import date
from io import StringIO
from pathlib import Path

# Nos ubicamos en la carpeta de este script, para que todo se cree aquí
# sin importar desde dónde lo ejecutes
os.chdir(Path(__file__).parent)

ZONA = Path("zona_practica")
if ZONA.exists():
    shutil.rmtree(ZONA)
ZONA.mkdir()

# Archivos de muestra para comprimir
(ZONA / "notas.txt").write_text("Repasar zipfile\n" * 50, encoding="utf-8")
(ZONA / "datos.csv").write_text(
    "nombre,edad\nAna,28\nCarlos,35\nMaría,22\n", encoding="utf-8"
)
(ZONA / "config.json").write_text(
    json.dumps({"tema": "oscuro", "idioma": "es"}, indent=2, ensure_ascii=False),
    encoding="utf-8",
)


# ============================================================================================

"""
El módulo zipfile
Las operaciones principales:

Operación                   Método
Crear ZIP                   ZipFile("archivo.zip", "w")
Agregar a ZIP existente     ZipFile("archivo.zip", "a")
Leer/extraer ZIP            ZipFile("archivo.zip", "r")
Listar contenido            .namelist()
Extraer todo                .extractall()
Extraer un archivo          .extract()
"""


# ============================================================================================

"""
Crear un archivo ZIP
ZIP básico — el modo "w" crea un ZIP nuevo (o sobrescribe uno existente).
Cada llamada a .write() agrega un archivo al ZIP.
"""

mi_zip = ZONA / "mi_archivo.zip"

with zipfile.ZipFile(mi_zip, "w") as zf:
    # El segundo argumento es el nombre dentro del ZIP (sin "zona_practica/")
    zf.write(ZONA / "notas.txt", "notas.txt")
    zf.write(ZONA / "datos.csv", "datos.csv")
    zf.write(ZONA / "config.json", "config.json")

print("ZIP creado con 3 archivos.")



# ZIP con compresión
# Por defecto, zipfile guarda los archivos SIN comprimir. Para comprimir: ZIP_DEFLATED

comprimido = ZONA / "comprimido.zip"

with zipfile.ZipFile(comprimido, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(ZONA / "notas.txt", "notas.txt")

print("ZIP comprimido creado.")

"""
Modo            Descripción
ZIP_STORED      Sin compresión (default) — solo agrupa
ZIP_DEFLATED    Compresión estándar — reduce tamaño

Para la mayoría de los casos, usa ZIP_DEFLATED.
"""



# Agregar archivos a un ZIP existente
# El modo "a" (append) agrega sin borrar los archivos que ya están dentro.

(ZONA / "archivo_nuevo.txt").write_text("Llegué después\n", encoding="utf-8")

with zipfile.ZipFile(mi_zip, "a") as zf:
    zf.write(ZONA / "archivo_nuevo.txt", "archivo_nuevo.txt")

print("Archivo agregado al ZIP existente.")



# Controlar la ruta dentro del ZIP
# Por defecto, zf.write("carpeta/datos.csv") guarda la ruta completa "carpeta/datos.csv".
# El segundo argumento de .write() cambia el nombre que tendrá dentro del ZIP.

(ZONA / "src" / "utils").mkdir(parents=True)
(ZONA / "src" / "main.py").write_text('print("main")\n', encoding="utf-8")
(ZONA / "src" / "utils" / "helpers.py").write_text("def ayudar(): pass\n", encoding="utf-8")

with zipfile.ZipFile(ZONA / "entrega.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(ZONA / "src" / "main.py", "main.py")
    zf.write(ZONA / "src" / "utils" / "helpers.py", "helpers.py")


# ============================================================================================

"""
Leer y extraer un ZIP
Listar el contenido con .namelist()
"""

with zipfile.ZipFile(mi_zip, "r") as zf:
    print("\nArchivos en el ZIP:")
    for nombre in zf.namelist():
        print(f"  {nombre}")

# Archivos en el ZIP:
#   notas.txt
#   datos.csv
#   config.json
#   archivo_nuevo.txt



# Información detallada con .infolist() — devuelve objetos ZipInfo

with zipfile.ZipFile(mi_zip, "r") as zf:
    print("\nSin compresión (mi_archivo.zip):")
    for info in zf.infolist():
        print(f"  {info.filename}: {info.file_size} → {info.compress_size} bytes")

with zipfile.ZipFile(comprimido, "r") as zf:
    print("\nCon ZIP_DEFLATED (comprimido.zip):")
    for info in zf.infolist():
        print(f"  {info.filename}: {info.file_size} → {info.compress_size} bytes")

# Fíjate: sin compresión los dos tamaños son iguales; con ZIP_DEFLATED el texto
# repetido de notas.txt queda muchísimo más pequeño.



# Extraer todo el contenido — si la carpeta destino no existe, la crea

with zipfile.ZipFile(mi_zip, "r") as zf:
    zf.extractall(ZONA / "carpeta_destino")

print("\nTodos los archivos extraídos.")



# Extraer un archivo específico

with zipfile.ZipFile(mi_zip, "r") as zf:
    zf.extract("datos.csv", ZONA / "solo_datos")

print("Solo 'datos.csv' fue extraído.")



# Leer sin extraer — útil cuando solo necesitas un dato rápido
# zf.open() devuelve bytes, por eso hay que .decode("utf-8")

with zipfile.ZipFile(mi_zip, "r") as zf:
    with zf.open("config.json") as f:
        contenido = f.read().decode("utf-8")
        config = json.loads(contenido)
        print(f"\nConfig leída desde el ZIP: {config}")


# ============================================================================================

"""
Ejemplo práctico: backup de archivos Python
Busca todos los .py de un proyecto y los comprime en un ZIP con fecha.
"""


def backup_python(carpeta_proyecto):
    """Crea un ZIP con todos los archivos .py de un proyecto."""
    proyecto = Path(carpeta_proyecto)

    if not proyecto.exists():
        print(f"Error: '{proyecto}' no existe.")
        return

    archivos_py = list(proyecto.rglob("*.py"))

    if not archivos_py:
        print("No se encontraron archivos .py")
        return

    fecha = date.today().isoformat()
    nombre_zip = ZONA / f"{proyecto.name}_python_backup_{fecha}.zip"

    with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for archivo in archivos_py:
            ruta_relativa = archivo.relative_to(proyecto)
            zf.write(archivo, ruta_relativa)
            print(f"  + {ruta_relativa.as_posix()}")

    tamano = nombre_zip.stat().st_size
    print(f"\nBackup creado: {nombre_zip.name}")
    print(f"Archivos: {len(archivos_py)}")
    print(f"Tamaño: {tamano / 1024:.1f} KB")


# Proyecto de prueba
mi_proyecto = ZONA / "mi_proyecto"
(mi_proyecto / "models").mkdir(parents=True)
(mi_proyecto / "main.py").write_text("# main\n", encoding="utf-8")
(mi_proyecto / "utils.py").write_text("# utils\n", encoding="utf-8")
(mi_proyecto / "models" / "usuario.py").write_text("# usuario\n", encoding="utf-8")
(mi_proyecto / "models" / "producto.py").write_text("# producto\n", encoding="utf-8")
(mi_proyecto / "README.txt").write_text("No es .py, no entra\n", encoding="utf-8")

print("\nBackup de archivos Python:")
backup_python(mi_proyecto)


# ============================================================================================

"""
Ejemplo práctico: extraer y procesar datos
Un ZIP descargado con varios CSV: los leemos sin extraerlos y generamos un resumen JSON.
Combina zipfile + csv + json — todo lo de la semana trabajando junto.

StringIO convierte un string en algo que se comporta como un archivo,
para que csv.DictReader pueda leerlo.
"""


def procesar_zip_datos(archivo_zip):
    """Lee los CSVs de un ZIP, procesa los datos y genera un resumen."""
    resultados = {}

    with zipfile.ZipFile(archivo_zip, "r") as zf:
        csvs = [f for f in zf.namelist() if f.endswith(".csv")]

        if not csvs:
            print("No se encontraron archivos CSV en el ZIP.")
            return

        print(f"Procesando {len(csvs)} archivo(s) CSV...\n")

        for nombre_csv in csvs:
            with zf.open(nombre_csv) as f:
                contenido = f.read().decode("utf-8")
                reader = csv.DictReader(StringIO(contenido))
                filas = list(reader)

                resultados[nombre_csv] = {
                    "filas": len(filas),
                    "columnas": list(filas[0].keys()) if filas else [],
                }

                print(f"  {nombre_csv}: {len(filas)} filas, "
                      f"{len(resultados[nombre_csv]['columnas'])} columnas")

    with open(ZONA / "resumen_zip.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print("\nResumen guardado en 'resumen_zip.json'")


# ZIP "descargado" de prueba
with zipfile.ZipFile(ZONA / "datos_descargados.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("ventas.csv", "producto,cantidad\nLaptop,3\nMouse,10\n")
    zf.writestr("clientes.csv", "nombre,ciudad,edad\nAna,CDMX,28\nLuis,Lima,40\nSofía,Bogotá,31\n")
    zf.writestr("leeme.txt", "Este no es CSV")

print()
procesar_zip_datos(ZONA / "datos_descargados.zip")


# ============================================================================================

"""
Troubleshooting
"""

# Problema 1: BadZipFile (archivo corrupto o que no es ZIP)
#
#   with zipfile.ZipFile("no_es_zip.txt", "r") as zf:
#       print(zf.namelist())
#   # zipfile.BadZipFile: File is not a zip file
#
# Causa: el archivo no es un ZIP válido, está corrupto, o tiene extensión .zip sin serlo.
# Solución: verifica antes con zipfile.is_zipfile()

falso = ZONA / "descarga.zip"
falso.write_text("Soy texto con extensión .zip", encoding="utf-8")

print()
for archivo in (falso, mi_zip):
    if zipfile.is_zipfile(archivo):
        with zipfile.ZipFile(archivo, "r") as zf:
            print(f"'{archivo.name}' es válido: {zf.namelist()}")
    else:
        print(f"'{archivo.name}' no es un archivo ZIP válido.")



# Problema 2: Rutas dentro del ZIP (archivos en subcarpetas inesperadas)
#
#   zf.write("/Users/mike/proyecto/main.py")
#
# Al extraer, aparece toda la ruta Users/mike/proyecto/main.py dentro del ZIP.
# Solución: segundo argumento de .write() + relative_to() de pathlib

proyecto = mi_proyecto.resolve()  # ruta absoluta, como en el ejemplo

with zipfile.ZipFile(ZONA / "proyecto.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    for archivo in proyecto.rglob("*.py"):
        zf.write(archivo, archivo.relative_to(proyecto))

with zipfile.ZipFile(ZONA / "proyecto.zip", "r") as zf:
    print(f"\nRutas limpias dentro del ZIP: {zf.namelist()}")



# Problema 3: Sobrescribir archivos al extraer
# extractall() sobrescribe archivos existentes sin avisar.
# Solución: revisar uno por uno antes de extraer.


def extraer_seguro(archivo_zip, destino="."):
    destino = Path(destino)

    with zipfile.ZipFile(archivo_zip, "r") as zf:
        for nombre in zf.namelist():
            ruta_destino = destino / nombre
            if ruta_destino.exists():
                print(f"  ⚠️  '{nombre}' ya existe, omitiendo.")
            else:
                zf.extract(nombre, destino)
                print(f"  ✓ '{nombre}' extraído.")


# solo_datos/ ya tiene datos.csv (lo extrajimos arriba), así que ese se omite
print("\nExtracción segura en solo_datos/:")
extraer_seguro(mi_zip, ZONA / "solo_datos")


# ============================================================================================

"""
Resumen
Operación           Código                          Modo
Crear ZIP           ZipFile("f.zip", "w")           "w" = escribir
Agregar a ZIP       ZipFile("f.zip", "a")           "a" = append
Abrir ZIP           ZipFile("f.zip", "r")           "r" = leer
Comprimir           zipfile.ZIP_DEFLATED            Reduce tamaño
Agregar archivo     zf.write("archivo.txt")         Dentro del with
Listar contenido    zf.namelist()                   Lista de nombres
Info detallada      zf.infolist()                   Objetos ZipInfo
Extraer todo        zf.extractall("destino")        Crea carpeta si no existe
Extraer uno         zf.extract("archivo.txt")       Un solo archivo
Verificar ZIP       zipfile.is_zipfile("f.zip")     True/False

Lo esencial: ZipFile con context manager (with), modo "w" para crear, modo "r" para leer,
ZIP_DEFLATED para comprimir. Con eso cubres el 90% de los casos.
"""
