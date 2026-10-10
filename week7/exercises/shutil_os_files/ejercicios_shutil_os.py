"""
Ejercicios — Operaciones con Archivos: shutil y os

! Como estos ejercicios mueven y renombran archivos, todo ocurre dentro de la carpeta
! zona_ejercicios/, que se borra y se vuelve a crear en cada ejecución.
"""

import os
import shutil
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
# Ejercicio 1: Copia de seguridad (Fácil)
# Copia datos.txt a backups/datos.txt. Si la carpeta backups no existe, créala primero.
# ============================================================================================

datos = ZONA / "datos.txt"
datos.write_text("Datos importantes\n", encoding="utf-8")

carpeta_backups = ZONA / "backups"
carpeta_backups.mkdir(exist_ok=True)

shutil.copy2(datos, carpeta_backups / "datos.txt")

print("Ejercicio 1:")
print(f"  ¿Existe el backup? {(carpeta_backups / 'datos.txt').exists()}")


# ============================================================================================
# Ejercicio 2: Renombrar archivos con patrón (Fácil)
# Renombra foto1.jpg, foto2.jpg, foto3.jpg a vacaciones_001.jpg, vacaciones_002.jpg, ...
# ============================================================================================

fotos = ZONA / "fotos"
fotos.mkdir()

for i in range(1, 4):
    (fotos / f"foto{i}.jpg").touch()

print("\nEjercicio 2:")
for i, foto in enumerate(sorted(fotos.glob("foto*.jpg")), start=1):
    nuevo_nombre = f"vacaciones_{i:03d}{foto.suffix}"
    foto.rename(fotos / nuevo_nombre)
    print(f"  {foto.name} → {nuevo_nombre}")


# ============================================================================================
# Ejercicio 3: Organizador de archivos por extensión (Medio)
# Recibe una carpeta como input y organiza los archivos en subcarpetas por extensión.
# Por ejemplo, los .txt van a txt/, los .py a py/, etc.
# ============================================================================================


def organizar_por_extension(ruta_carpeta):
    """Mueve cada archivo a una subcarpeta con el nombre de su extensión."""
    carpeta = Path(ruta_carpeta)

    if not carpeta.is_dir():
        print(f"'{carpeta}' no existe o no es una carpeta.")
        return

    conteo = {}

    for archivo in [f for f in carpeta.iterdir() if f.is_file()]:
        extension = archivo.suffix.lower().lstrip(".") or "sin_extension"
        destino = carpeta / extension
        destino.mkdir(exist_ok=True)

        shutil.move(archivo, destino / archivo.name)
        conteo[extension] = conteo.get(extension, 0) + 1

    for extension, cantidad in sorted(conteo.items()):
        print(f"  {extension}/: {cantidad} archivo(s)")


mezclados = ZONA / "mezclados"
mezclados.mkdir()

for nombre in ["notas.txt", "app.py", "datos.csv", "readme.txt", "utils.py", "LICENSE"]:
    (mezclados / nombre).touch()

print("\nEjercicio 3:")
organizar_por_extension(mezclados)

# Para pedir la carpeta al usuario, descomenta estas líneas:
# ruta = input("¿Qué carpeta quieres organizar? ")
# organizar_por_extension(ruta)


# ============================================================================================
# Ejercicio 4: Script de backup con fecha (Medio)
# Copia una carpeta de proyecto completa a un backup con la fecha de hoy en el nombre.
# Formato: proyecto_backup_2025-06-15/
# ============================================================================================

proyecto = ZONA / "proyecto"
(proyecto / "src").mkdir(parents=True)
(proyecto / "src" / "main.py").write_text("print('Hola')\n", encoding="utf-8")
(proyecto / "README.txt").write_text("Mi proyecto\n", encoding="utf-8")

hoy = date.today().isoformat()  # 2025-06-15
backup = ZONA / f"proyecto_backup_{hoy}"

# dirs_exist_ok=True para que no falle si ya hiciste un backup hoy
shutil.copytree(proyecto, backup, dirs_exist_ok=True)

print("\nEjercicio 4:")
print(f"  Backup creado en '{backup}':")
for archivo in sorted(backup.rglob("*")):
    print(f"    {archivo.relative_to(backup)}")
