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