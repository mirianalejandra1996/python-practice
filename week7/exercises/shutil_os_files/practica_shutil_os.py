"""
Semana 7: Archivos y Formatos de Datos
Operaciones con Archivos: shutil y os

Ya sabes leer y escribir archivos. Pero en el mundo real necesitas hacer mucho más:
copiar un archivo para hacer un backup, mover archivos a otra carpeta, renombrar un lote
de archivos con un patrón consistente, o eliminar archivos que ya no necesitas.

- shutil (shell utilities) → operaciones de alto nivel como copiar y mover
- os                       → operaciones de bajo nivel
- pathlib                  → lo combinamos con los dos anteriores

! Como esta práctica mueve y elimina archivos, todo ocurre dentro de la carpeta
! zona_practica/, que se borra y se vuelve a crear en cada ejecución.
"""

import os
import shutil
from pathlib import Path

# Nos ubicamos en la carpeta de este script, para que todo se cree aquí
# sin importar desde dónde lo ejecutes
os.chdir(Path(__file__).parent)

ZONA = Path("zona_practica")
if ZONA.exists():
    shutil.rmtree(ZONA)
ZONA.mkdir()


# ============================================================================================

"""
Más allá de leer y escribir
Los archivos también son objetos en tu sistema de archivos que puedes manipular:

Operación           ¿Cuándo la necesitas?
Copiar              Backups, duplicar plantillas
Mover               Organizar archivos, renombrar con nueva ubicación
Renombrar           Estandarizar nombres, agregar prefijos/sufijos
Eliminar            Limpiar archivos temporales, logs viejos
Copiar carpetas     Backups completos de proyectos
Eliminar carpetas   Limpiar carpetas de cache o builds
"""


# ============================================================================================

"""
El módulo shutil
Copiar archivos
"""

reporte = ZONA / "reporte.txt"
reporte.write_text("Reporte de ventas\n", encoding="utf-8")

(ZONA / "backups").mkdir()

shutil.copy(reporte, ZONA / "reporte_copia.txt")   # copia con otro nombre
shutil.copy(reporte, ZONA / "backups")             # copia dentro de una carpeta

# shutil.copy() copia el contenido y los permisos, pero no los metadatos
# (fecha de creación, fecha de modificación). Para preservarlos:
shutil.copy2(reporte, ZONA / "reporte_copia2.txt")

"""
Función         Copia contenido     Copia permisos      Copia metadatos
shutil.copy()   ✓                   ✓                   ✗
shutil.copy2()  ✓                   ✓                   ✓
"""



# Mover y renombrar archivos

(ZONA / "archivos").mkdir()

shutil.move(ZONA / "reporte_copia.txt", ZONA / "archivos" / "reporte.txt")        # mover
shutil.move(ZONA / "reporte_copia2.txt", ZONA / "informe_final.txt")              # renombrar
shutil.move(ZONA / "informe_final.txt", ZONA / "archivos" / "informe_final.txt")  # mover y renombrar

# shutil.move() funciona como "cortar y pegar" — el archivo desaparece de su ubicación original.

print("Contenido de zona_practica/archivos/:")
for archivo in sorted((ZONA / "archivos").iterdir()):
    print(f"  {archivo.name}")



# Copiar carpetas completas

proyecto = ZONA / "mi_proyecto"
(proyecto / "datos").mkdir(parents=True)
(proyecto / "main.py").write_text("print('Hola')\n", encoding="utf-8")
(proyecto / "datos" / "ventas.csv").write_text("producto,total\nCafé,450\n", encoding="utf-8")

shutil.copytree(proyecto, ZONA / "mi_proyecto_backup")

# copytree() copia toda la estructura, incluyendo subdirectorios y archivos.
# La carpeta destino no debe existir (la crea automáticamente).
# Con dirs_exist_ok=True (Python 3.8+), si la carpeta destino ya existe, se mezclan los contenidos:

shutil.copytree(proyecto, ZONA / "mi_proyecto_backup", dirs_exist_ok=True)

print("\nBackup del proyecto:")
for archivo in sorted((ZONA / "mi_proyecto_backup").rglob("*")):
    print(f"  {archivo.relative_to(ZONA)}")



# Eliminar carpetas (¡con cuidado!)

temporal = ZONA / "carpeta_temporal"
temporal.mkdir()
(temporal / "cache.tmp").touch()

shutil.rmtree(temporal)
print(f"\n¿Existe {temporal.name}? {temporal.exists()}")

"""
! ADVERTENCIA: shutil.rmtree() elimina la carpeta y todo su contenido de forma
! permanente. No va a la papelera de reciclaje. No hay Ctrl+Z.
! Piensa dos veces antes de usarlo.
"""


def eliminar_con_confirmacion(ruta):
    """Elimina una carpeta solo si el usuario confirma."""
    carpeta = Path(ruta)

    if carpeta.exists():
        confirmacion = input(f"¿Eliminar '{carpeta}' y todo su contenido? (s/n): ")
        if confirmacion.lower() == "s":
            shutil.rmtree(carpeta)
            print("Carpeta eliminada.")
        else:
            print("Operación cancelada.")
    else:
        print("La carpeta no existe.")


# Para probarlo de forma interactiva, descomenta esta línea:
# eliminar_con_confirmacion(ZONA / "mi_proyecto_backup")


# ============================================================================================

"""
Operaciones con os
Operaciones más básicas a nivel del sistema operativo.
"""

# Renombrar
viejo = ZONA / "archivo_viejo.txt"
viejo.touch()
os.rename(viejo, ZONA / "archivo_nuevo.txt")

# Eliminar un archivo (si no existe, lanza FileNotFoundError)
temporal = ZONA / "archivo_temporal.txt"
temporal.touch()
os.remove(temporal)

# Eliminar un directorio vacío (si tiene archivos dentro, lanza OSError)
vacia = ZONA / "carpeta_vacia"
vacia.mkdir()
os.rmdir(vacia)

print(f"\n¿Existe archivo_nuevo.txt? {(ZONA / 'archivo_nuevo.txt').exists()}")
print(f"¿Existe archivo_temporal.txt? {temporal.exists()}")
print(f"¿Existe carpeta_vacia? {vacia.exists()}")


# ============================================================================================

"""
Equivalentes con pathlib
"""

archivo = ZONA / "reporte_pathlib.txt"
archivo.touch()

archivo = archivo.rename(ZONA / "informe_pathlib.txt")   # renombrar (retorna la nueva ruta)
archivo.unlink()                                         # eliminar archivo

carpeta = ZONA / "temp"
carpeta.mkdir()
carpeta.rmdir()                                          # eliminar directorio vacío

"""
¿Cuándo usar cada uno?

Operación               shutil              os              pathlib
Copiar archivo          shutil.copy()       —               —
Copiar con metadatos    shutil.copy2()      —               —
Mover archivo           shutil.move()       —               —
Renombrar               —                   os.rename()     path.rename()
Eliminar archivo        —                   os.remove()     path.unlink()
Eliminar dir vacío      —                   os.rmdir()      path.rmdir()
Copiar carpeta          shutil.copytree()   —               —
Eliminar carpeta        shutil.rmtree()     —               —

! La regla práctica: shutil para copiar/mover, pathlib para renombrar/eliminar.
"""


# ============================================================================================

"""
Ejemplo práctico: organizador de descargas
El script estrella de la cápsula: organiza una carpeta de descargas en subcarpetas
por tipo de archivo.
"""

CARPETA_DESCARGAS = ZONA / "descargas"

CATEGORIAS = {
    "imagenes": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "documentos": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"],
    "codigo": [".py", ".js", ".html", ".css", ".json", ".csv"],
    "comprimidos": [".zip", ".rar", ".tar", ".gz"],
    "videos": [".mp4", ".avi", ".mov", ".mkv"],
}


def obtener_categoria(extension):
    """Retorna la categoría de un archivo según su extensión."""
    for categoria, extensiones in CATEGORIAS.items():
        if extension.lower() in extensiones:
            return categoria
    return "otros"


def organizar_descargas():
    """Organiza archivos de la carpeta de descargas en subcarpetas."""
    if not CARPETA_DESCARGAS.exists():
        print(f"La carpeta '{CARPETA_DESCARGAS}' no existe.")
        return

    archivos = [f for f in CARPETA_DESCARGAS.iterdir() if f.is_file()]

    if not archivos:
        print("No hay archivos para organizar.")
        return

    conteo = {}

    for archivo in archivos:
        categoria = obtener_categoria(archivo.suffix)
        carpeta_destino = CARPETA_DESCARGAS / categoria

        carpeta_destino.mkdir(exist_ok=True)

        destino = carpeta_destino / archivo.name
        shutil.move(str(archivo), str(destino))

        conteo[categoria] = conteo.get(categoria, 0) + 1

    print("Organización completada:\n")
    for categoria, cantidad in sorted(conteo.items()):
        print(f"  📁 {categoria}: {cantidad} archivo(s)")
    print(f"\n  Total: {sum(conteo.values())} archivos organizados")



# Para probarlo, creamos una carpeta con archivos de ejemplo

CARPETA_DESCARGAS.mkdir(exist_ok=True)

archivos_ejemplo = [
    "foto_vacaciones.jpg", "reporte_anual.pdf", "script.py",
    "datos.csv", "presentacion.pptx", "backup.zip",
    "video_tutorial.mp4", "notas.txt", "logo.png",
    "app.js", "estilos.css", "foto2.jpeg"
]

for nombre in archivos_ejemplo:
    (CARPETA_DESCARGAS / nombre).touch()

print(f"\nCreados {len(archivos_ejemplo)} archivos de ejemplo en '{CARPETA_DESCARGAS}/'\n")

organizar_descargas()


# ============================================================================================

"""
Buenas prácticas de seguridad
Cuando manipulas archivos, un error puede significar perder datos.
"""

# 1. Siempre verifica antes de actuar

archivo = ZONA / "datos_importantes.csv"

if archivo.exists():
    archivo.unlink()
    print("\nArchivo eliminado.")
else:
    print("\nEl archivo no existe.")



# 2. Crea backups antes de operaciones masivas

carpeta = ZONA / "mi_proyecto"

if carpeta.exists():
    backup = ZONA / "mi_proyecto_backup_2"
    shutil.copytree(carpeta, backup)
    print(f"Backup creado en '{backup}'")



# 3. Usa try/except para operaciones riesgosas

try:
    shutil.move(ZONA / "archivo.txt", ZONA / "destino" / "archivo.txt")
    print("Archivo movido correctamente.")
except FileNotFoundError:
    print("Error: el archivo origen no existe.")
except PermissionError:
    print("Error: no tienes permisos para esta operación.")
except shutil.Error as e:
    print(f"Error al mover: {e}")


# ============================================================================================
# TROUBLESHOOTING
# ============================================================================================

# Problema 1: PermissionError al manipular archivos del sistema

# os.remove("/etc/hosts")
# PermissionError: [Errno 13] Permission denied: '/etc/hosts'

# Causa: estás intentando modificar un archivo protegido por el sistema operativo
# o que pertenece a otro usuario.
# Solución: solo trabaja con archivos dentro de tu directorio de proyecto.

archivo = ZONA / "datos.txt"
archivo.touch()

if archivo.exists():
    try:
        archivo.unlink()
        print("\nArchivo eliminado.")
    except PermissionError:
        print(f"Sin permisos para eliminar '{archivo}'.")



# Problema 2: El destino ya existe al copiar/mover

original = ZONA / "original.txt"
original.write_text("Versión 1\n", encoding="utf-8")

shutil.copy(original, ZONA / "copia.txt")  # Primera vez: OK
original.write_text("Versión 2\n", encoding="utf-8")
shutil.copy(original, ZONA / "copia.txt")  # Segunda vez: sobrescribe sin avisar

print(f"Contenido de copia.txt: {(ZONA / 'copia.txt').read_text(encoding='utf-8').strip()}")

# Causa: shutil.copy() sobrescribe archivos sin preguntar. shutil.copytree() falla si
# la carpeta destino ya existe (a menos que uses dirs_exist_ok=True).
# Solución: verifica antes de copiar si quieres evitar sobrescrituras:


def copiar_sin_sobrescribir(origen, destino):
    """Copia un archivo y pide confirmación si el destino ya existe."""
    origen = Path(origen)
    destino = Path(destino)

    if destino.exists():
        print(f"'{destino}' ya existe. ¿Sobrescribir? (s/n)")
        if input().strip().lower() != "s":
            print("Operación cancelada.")
        else:
            shutil.copy2(origen, destino)
            print("Archivo copiado (sobrescrito).")
    else:
        shutil.copy2(origen, destino)
        print("Archivo copiado.")


# Para probarlo de forma interactiva, descomenta esta línea:
# copiar_sin_sobrescribir(original, ZONA / "copia.txt")



# Problema 3: shutil.rmtree() es PERMANENTE

# shutil.rmtree("mi_proyecto")   # ¡PELIGRO! Elimina TODO sin posibilidad de recuperación

# Causa: shutil.rmtree() no envía archivos a la papelera. Los elimina directamente del disco.
# Solución: siempre pide confirmación y muestra qué se va a eliminar:


def eliminar_seguro(carpeta_path):
    carpeta = Path(carpeta_path)

    if not carpeta.exists():
        print(f"'{carpeta}' no existe.")
        return

    archivos = list(carpeta.rglob("*"))
    num_archivos = len([f for f in archivos if f.is_file()])

    print(f"⚠️  Vas a eliminar '{carpeta}' con {num_archivos} archivo(s).")
    print("Esta operación es PERMANENTE.")
    confirmacion = input("Escribe 'ELIMINAR' para confirmar: ")

    if confirmacion == "ELIMINAR":
        shutil.rmtree(carpeta)
        print("Carpeta eliminada.")
    else:
        print("Operación cancelada.")


# Para probarlo de forma interactiva, descomenta esta línea:
# eliminar_seguro(ZONA / "mi_proyecto_backup_2")


"""
Resumen

Operación           Función                             Módulo
Copiar archivo      shutil.copy() / shutil.copy2()      shutil
Mover archivo       shutil.move()                       shutil
Copiar carpeta      shutil.copytree()                   shutil
Eliminar carpeta    shutil.rmtree()                     shutil
Renombrar           path.rename()                       pathlib
Eliminar archivo    path.unlink()                       pathlib
Eliminar dir vacío  path.rmdir()                        pathlib

! Lo esencial: shutil para copiar y mover, pathlib para renombrar y eliminar.
! Siempre verifica con Path.exists() antes de operar, y nunca uses rmtree() sin confirmación.
"""
