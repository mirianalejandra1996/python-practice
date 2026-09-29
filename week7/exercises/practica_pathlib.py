# from pathlib import Path

# ruta = Path("mi_archivo.txt")
# print(ruta)        # mi_archivo.txt
# print(type(ruta))  # <class 'pathlib.PosixPath'> (o WindowsPath en Windows)


from pathlib import Path

actual = Path.cwd()
print(f"Directorio actual: {actual}")
# /Users/ana/proyectos/mi_script

home = Path.home()
print(f"Directorio home: {home}")
# /Users/ana

"""
Path.cwd() → el directorio desde donde ejecutas el script (Current Working Directory)
Path.home() → el directorio home del usuario
"""

ruta = Path("proyecto") / "datos" / "raw" / "ventas.csv"
print(ruta)


# ============================================================================================

"""
Operaciones con Path
Información sobre una ruta
"""

from pathlib import Path

ruta = Path("proyecto/datos/reporte_2025.csv")

print(ruta.name)    # reporte_2025.csv    (nombre completo del archivo)
print(ruta.stem)    # reporte_2025        (nombre sin extensión)
print(ruta.suffix)  # .csv                (extensión)
print(ruta.parent)  # proyecto/datos      (directorio padre)




# Estos atributos son muy útiles para procesar archivos:

archivo = Path("datos/ventas_enero.csv")

nuevo_nombre = archivo.stem + "_procesado" + archivo.suffix
print(nuevo_nombre)  # ventas_enero_procesado.csv



# Verificar existencia:

ruta = Path("mi_archivo.txt")
print(ruta)

print(ruta.exists())   # True o False — ¿existe?
print(ruta.is_file())  # True o False — ¿es un archivo?
print(ruta.is_dir())   # True o False — ¿es un directorio?



# Antes de leer un archivo, verifica que existe:

archivo = Path("datos.txt")

if archivo.exists():
    with open(archivo, "r") as f:
        contenido = f.read()
    print(contenido)
else:
    print(f"El archivo {archivo} no existe.")
    
    
    
# Crear directorios

carpeta = Path("proyecto/datos/raw")
carpeta.mkdir(parents=True, exist_ok=True)

# Path("proyecto/datos/raw").mkdir()   # comentado: falla porque ya lo creamos arriba
# FileNotFoundError si "proyecto/datos/" no existe
# FileExistsError si "proyecto/datos/raw/" ya existe

"""
! Siempre usa parents=True, exist_ok=True a menos que tengas una razón
! específica para no hacerlo.

"""


# ============================================================================================

"""
Iterar archivos
.iterdir() — listar contenido de un directorio
"""

from pathlib import Path

directorio = Path(".")

for item in directorio.iterdir():
    tipo = "📁" if item.is_dir() else "📄"
    print(f"{tipo} {item.name}")

# .iterdir() lista todo el contenido: archivos y subdirectorios.



# .glob() — buscar archivos por patrón

directorio = Path(".")

for archivo in directorio.glob("*.txt"):
    print(archivo.name)

"""
Patrones comunes:

Patrón          Encuentra
"*.txt"         Todos los archivos .txt en el directorio
"*.py"          Todos los archivos .py en el directorio
"reporte_*"     Archivos que empiezan con "reporte_"
"*.csv"         Todos los archivos .csv en el directorio
"""



# .rglob() — búsqueda recursiva

proyecto = Path(".")

for archivo_py in proyecto.rglob("*.py"):
    print(archivo_py)

# .rglob() busca en el directorio y todos sus subdirectorios. La "r" significa "recursive".

base = Path("proyecto")

todos_los_csv = list(base.rglob("*.csv"))
print(f"Encontré {len(todos_los_csv)} archivos CSV:")
for csv in todos_los_csv:
    print(f"  {csv}")



# Leer y escribir con pathlib (sin usar open())

archivo = Path("mensaje.txt")

archivo.write_text("Hola desde pathlib\n", encoding="utf-8")

contenido = archivo.read_text(encoding="utf-8")
print(contenido)

"""
Para archivos pequeños, .read_text() y .write_text() son convenientes.
Para archivos grandes o procesamiento línea por línea, sigue usando open()
con context managers.
"""


# ============================================================================================

"""
Módulo os: la forma clásica
Antes de pathlib (Python 3.4+), el módulo os era la única opción.
Todavía lo vas a ver en código existente, así que es útil conocerlo.
"""

import os

print(os.getcwd())                  # directorio actual
print(os.listdir("."))              # lista de archivos y carpetas
print(os.path.exists("datos.txt"))  # ¿existe?
print(os.path.isfile("datos.txt"))  # ¿es archivo?
print(os.path.isdir("datos"))       # ¿es directorio?



# Construir rutas con os.path.join()

ruta = os.path.join("proyecto", "datos", "raw", "ventas.csv")
print(ruta)
# proyecto/datos/raw/ventas.csv (en Mac/Linux)
# proyecto\datos\raw\ventas.csv (en Windows)



# Crear directorios con os.makedirs()

os.makedirs("proyecto/datos/raw", exist_ok=True)

"""
Pathlib vs os.path: comparación directa

Operación           pathlib                         os / os.path
Directorio actual   Path.cwd()                      os.getcwd()
Directorio home     Path.home()                     os.path.expanduser("~")
Construir ruta      Path("a") / "b" / "c"           os.path.join("a", "b", "c")
¿Existe?            path.exists()                   os.path.exists(path)
¿Es archivo?        path.is_file()                  os.path.isfile(path)
¿Es directorio?     path.is_dir()                   os.path.isdir(path)
Nombre              path.name                       os.path.basename(path)
Extensión           path.suffix                     os.path.splitext(path)[1]
Directorio padre    path.parent                     os.path.dirname(path)
Crear directorio    path.mkdir(parents=True)        os.makedirs(path)
Listar contenido    path.iterdir()                  os.listdir(path)
Buscar por patrón   path.glob("*.txt")              glob.glob("*.txt")

! Recomendación: usa pathlib para código nuevo. Es más legible, más Pythónico
! y más seguro entre sistemas operativos. Solo usa os si trabajas con código
! existente que ya lo usa.
"""


# ============================================================================================
# EJERCICIOS
# ============================================================================================

# Ejercicio 1: Explorar tu directorio (Fácil)

print(f"\nDirectorio actual: {Path.cwd()}")

for item in Path.cwd().iterdir():
    tipo = "Directorio" if item.is_dir() else "Archivo"
    print(f"  [{tipo}] {item.name}")



# Ejercicio 2: Crear estructura de directorios (Fácil)
"""
mi_proyecto/
├── datos/
│   ├── raw/
│   └── processed/
├── scripts/
└── reportes/
"""

raiz = Path("mi_proyecto")

carpetas = [
    raiz / "datos" / "raw",
    raiz / "datos" / "processed",
    raiz / "scripts",
    raiz / "reportes",
]

for carpeta in carpetas:
    carpeta.mkdir(parents=True, exist_ok=True)

print("\nVerificando estructura:")
for carpeta in [raiz, raiz / "datos", *carpetas]:
    estado = "OK" if carpeta.is_dir() else "FALTA"
    print(f"  {estado}  {carpeta}")



# Ejercicio 3: Encontrar archivos por extensión (Medio)

carpeta = Path("prueba_glob")
carpeta.mkdir(exist_ok=True)

archivos_ejemplo = [
    "notas.txt", "datos.csv", "script.py",
    "readme.txt", "config.json", "diario.txt",
    "reporte.csv", "utils.py",
]

for nombre in archivos_ejemplo:
    archivo = carpeta / nombre
    archivo.write_text(f"Contenido de {nombre}\n", encoding="utf-8")

print(f"\nArchivos creados en {carpeta}/\n")

print("Archivos .txt encontrados:")
for txt in sorted(carpeta.glob("*.txt")):
    print(f"  {txt.name}")

print(f"\nArchivos .py encontrados:")
for py in sorted(carpeta.glob("*.py")):
    print(f"  {py.name}")

print(f"\nArchivos .csv encontrados:")
for csv_file in sorted(carpeta.glob("*.csv")):
    print(f"  {csv_file.name}")

print(f"\nTotal de archivos: {len(list(carpeta.iterdir()))}")



# Ejercicio 4: Organizador de archivos por extensión (Medio)
# Usa los archivos de prueba_glob/ del ejercicio 3

import shutil

origen = Path("prueba_glob")

destinos = {
    ".txt": origen / "textos",
    ".csv": origen / "datos",
    ".py": origen / "scripts",
}

for destino in destinos.values():
    destino.mkdir(exist_ok=True)

organizados = 0
for archivo in origen.iterdir():
    if archivo.is_file() and archivo.suffix in destinos:
        shutil.copy2(archivo, destinos[archivo.suffix] / archivo.name)
        organizados += 1

print(f"\nOrganicé {organizados} archivos:")
for extension, destino in destinos.items():
    cantidad = len(list(destino.glob(f"*{extension}")))
    print(f"  {destino.name}/: {cantidad} archivos {extension}")


# ============================================================================================
# TROUBLESHOOTING
# ============================================================================================

# Problema 1: Rutas que no funcionan entre sistemas operativos

# ruta = "datos\nuevo\archivo.txt"
# En Windows, \n dentro del string se interpreta como salto de línea,
# no como separador de directorio. Tu ruta se corrompe.

# Solución: nunca construyas rutas con strings. Usa pathlib:
ruta = Path("datos") / "nuevo" / "archivo.txt"
print(ruta)

# Si necesitas un string con ruta de Windows, usa raw strings:
ruta = r"datos\nuevo\archivo.txt"
print(ruta)



# Problema 2: PermissionError al acceder a directorios del sistema

# sistema = Path("/usr/local/bin")
# for archivo in sistema.iterdir():
#     print(archivo)
# PermissionError: [Errno 13] Permission denied

# Causa: estás intentando acceder a un directorio que requiere permisos de administrador.
# Solución: trabaja dentro de tu directorio home o directorios donde tengas permisos:

mi_espacio = Path.home() / "mis_proyectos"
mi_espacio.mkdir(exist_ok=True)



# Problema 3: Rutas relativas vs absolutas

relativa = Path("datos/archivo.txt")
print(relativa)            # datos/archivo.txt
print(relativa.resolve())  # C:\Users\...\datos\archivo.txt (ruta absoluta)

"""
Rutas relativas dependen del directorio desde donde ejecutas el script.
Rutas absolutas siempre apuntan al mismo lugar, sin importar desde dónde ejecutes.

Buena práctica: usa rutas relativas dentro de tu proyecto (portabilidad)
y .resolve() cuando necesites la ruta absoluta.
"""

base = Path(__file__).parent
datos = base / "datos" / "archivo.txt"
print(datos)
# Path(__file__).parent te da el directorio donde está tu script .py,
# sin importar desde dónde lo ejecutes.


"""
Resumen
- pathlib.Path es la forma moderna de trabajar con rutas — orientada a objetos y multiplataforma
- El operador / construye rutas: Path("a") / "b" / "c.txt"
- Path.cwd() → directorio actual, Path.home() → directorio home
- .exists(), .is_file(), .is_dir() verifican la existencia
- .name, .stem, .suffix, .parent extraen partes de la ruta
- .mkdir(parents=True, exist_ok=True) crea directorios de forma segura
- .iterdir() lista contenido, .glob() busca por patrón, .rglob() busca recursivamente
- El módulo os es la alternativa clásica — funcional pero menos legible que pathlib
- Usa pathlib para código nuevo. Usa os solo con código legacy
"""
