# Tracker de Gastos Personal — Python Mini-Bootcamp Semana 7
import csv
import json
import shutil
import zipfile
from datetime import date, datetime
from pathlib import Path

# --- Rutas del proyecto ---
RAIZ = Path(__file__).parent
CARPETA_DATOS = RAIZ / "datos"
CARPETA_EXPORTS = RAIZ / "exports"
CARPETA_BACKUPS = RAIZ / "backups"

ARCHIVO_LOG = CARPETA_DATOS / "log.txt"
ARCHIVO_JSON = CARPETA_DATOS / "gastos.json"


# =============================================================
# Fase 1 — Estructura de carpetas con pathlib
# =============================================================

def preparar_carpetas():
    """Crea las carpetas del proyecto si no existen."""
    for carpeta in (CARPETA_DATOS, CARPETA_EXPORTS, CARPETA_BACKUPS):
        carpeta.mkdir(parents=True, exist_ok=True)
        print(f"  Carpeta lista: {carpeta.name}/")

    # Ejercicio en vivo 1: subcarpeta del año actual dentro de exports/
    carpeta_anio = CARPETA_EXPORTS / str(date.today().year)
    carpeta_anio.mkdir(parents=True, exist_ok=True)
    print(f"  Carpeta lista: exports/{carpeta_anio.name}/")


def mostrar_contenido_proyecto():
    """Lista lo que hay en la raíz del proyecto."""
    print(f"\n  Proyecto en: {RAIZ}")
    for item in sorted(RAIZ.iterdir()):
        marca = "[DIR]" if item.is_dir() else "[FILE]"
        print(f"  {marca} {item.name}")


# =============================================================
# Fase 2 — Log de gastos en TXT
# =============================================================

def registrar_gasto_txt(monto, categoria, descripcion):
    """Agrega una línea al log de gastos."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    linea = f"{fecha} | ${monto:.2f} | {categoria} | {descripcion}\n"

    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linea)

    print(f"  Registrado en log: {linea.strip()}")


def mostrar_log():
    """Imprime todas las líneas del log de gastos."""
    if not ARCHIVO_LOG.exists():
        print("  Aún no hay gastos registrados.")
        return

    print("\n  --- Log de gastos ---")
    with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
        for i, linea in enumerate(f, start=1):
            print(f"  {i}. {linea.strip()}")


def total_log():
    """Ejercicio en vivo 2: suma todos los montos del log.txt."""
    if not ARCHIVO_LOG.exists():
        return 0.0

    total = 0.0
    with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.split("|")
            if len(partes) < 2:
                continue  # línea vacía o mal formada
            monto_texto = partes[1].strip().replace("$", "")
            total += float(monto_texto)
    return total


# =============================================================
# Fase 3 — JSON (estructura real)
# =============================================================

def cargar_gastos():
    """Carga la lista de gastos desde JSON. Si no existe, retorna lista vacía."""
    if not ARCHIVO_JSON.exists():
        return []

    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("  Archivo corrupto. Empezando de cero.")
        return []


def guardar_gastos(gastos):
    """Guarda la lista de gastos en JSON con formato legible."""
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=2, ensure_ascii=False)


def agregar_gasto(monto, categoria, descripcion):
    """Agrega un gasto nuevo al archivo JSON (y lo anota en el log TXT)."""
    gastos = cargar_gastos()

    # Usamos el id más alto + 1 para no repetir ids si se eliminó algún gasto
    siguiente_id = max((g["id"] for g in gastos), default=0) + 1

    nuevo = {
        "id": siguiente_id,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "monto": float(monto),
        "categoria": categoria,
        "descripcion": descripcion,
    }

    gastos.append(nuevo)
    guardar_gastos(gastos)
    registrar_gasto_txt(nuevo["monto"], categoria, descripcion)

    print(f"  Gasto #{nuevo['id']} agregado: ${nuevo['monto']:.2f} en {categoria}")
    return nuevo


def mostrar_gastos(gastos):
    """Imprime una lista de gastos en formato de tabla."""
    if not gastos:
        print("  No hay gastos registrados.")
        return

    print(f"\n  --- {len(gastos)} gasto(s) registrado(s) ---")
    for g in gastos:
        print(f"  #{g['id']:<3} {g['fecha']}  ${g['monto']:>8.2f}  "
              f"{g['categoria']:<15} {g['descripcion']}")


def resumen_por_categoria():
    """Calcula el total gastado en cada categoría."""
    gastos = cargar_gastos()
    if not gastos:
        print("  No hay gastos para resumir.")
        return

    totales = {}
    for g in gastos:
        cat = g["categoria"]
        totales[cat] = totales.get(cat, 0) + g["monto"]

    print("\n  --- Resumen por categoría ---")
    for cat, total in sorted(totales.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:<15} ${total:>10.2f}")


def eliminar_gasto(id_gasto):
    """Ejercicio en vivo 3: elimina un gasto del JSON por su id."""
    gastos = cargar_gastos()
    restantes = [g for g in gastos if g["id"] != id_gasto]

    if len(restantes) == len(gastos):
        print(f"  No existe un gasto con id #{id_gasto}.")
        return False

    guardar_gastos(restantes)
    print(f"  Gasto #{id_gasto} eliminado.")
    return True


# =============================================================
# Fase 4 — Exportar a CSV
# =============================================================

CAMPOS_CSV = ["id", "fecha", "monto", "categoria", "descripcion"]


def gastos_del_mes(anio, mes):
    """Reto A: devuelve solo los gastos del año-mes indicado."""
    prefijo = f"{anio}-{mes:02d}"
    return [g for g in cargar_gastos() if g["fecha"].startswith(prefijo)]


def escribir_csv(ruta, gastos):
    """Escribe una lista de gastos en un CSV con encabezados."""
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        writer.writeheader()
        writer.writerows(gastos)


def exportar_csv_mes(anio, mes):
    """Exporta todos los gastos del mes indicado a un CSV."""
    if not cargar_gastos():
        print("  No hay gastos para exportar.")
        return None

    prefijo = f"{anio}-{mes:02d}"
    del_mes = gastos_del_mes(anio, mes)

    if not del_mes:
        print(f"  No hay gastos en {prefijo}.")
        return None

    nombre_archivo = CARPETA_EXPORTS / f"gastos_{prefijo}.csv"
    escribir_csv(nombre_archivo, del_mes)

    print(f"  Exportados {len(del_mes)} gastos a {nombre_archivo.name}")
    return nombre_archivo


def exportar_por_categoria(categoria):
    """Ejercicio en vivo 4: exporta solo los gastos de una categoría."""
    de_categoria = [g for g in cargar_gastos()
                    if g["categoria"].lower() == categoria.lower()]

    if not de_categoria:
        print(f"  No hay gastos en la categoría '{categoria}'.")
        return None

    nombre_archivo = CARPETA_EXPORTS / f"gastos_{categoria.lower()}.csv"
    escribir_csv(nombre_archivo, de_categoria)

    print(f"  Exportados {len(de_categoria)} gastos a {nombre_archivo.name}")
    return nombre_archivo


def total_desde_csv(ruta_csv):
    """Lee un CSV exportado y devuelve el total gastado."""
    total = 0.0
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            total += float(fila["monto"])
    return total


# =============================================================
# Fase 5 — Backup ZIP, shutil y menú
# =============================================================

def crear_backup():
    """Crea un ZIP con todos los datos y exports actuales."""
    fecha = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    nombre_zip = CARPETA_BACKUPS / f"backup_{fecha}.zip"

    archivos_a_incluir = []
    if ARCHIVO_JSON.exists():
        archivos_a_incluir.append(ARCHIVO_JSON)
    if ARCHIVO_LOG.exists():
        archivos_a_incluir.append(ARCHIVO_LOG)
    archivos_a_incluir.extend(CARPETA_EXPORTS.rglob("*.csv"))

    if not archivos_a_incluir:
        print("  No hay archivos para respaldar.")
        return None

    with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for archivo in archivos_a_incluir:
            ruta_dentro_del_zip = archivo.relative_to(RAIZ)
            zf.write(archivo, ruta_dentro_del_zip)

    tamano_kb = nombre_zip.stat().st_size / 1024
    print(f"  Backup creado: {nombre_zip.name} ({tamano_kb:.1f} KB)")
    print(f"  Archivos incluidos: {len(archivos_a_incluir)}")
    return nombre_zip


def archivar_exports():
    """Mueve los CSVs de exports/ a una subcarpeta exports/archivo/."""
    archivo_dir = CARPETA_EXPORTS / "archivo"
    archivo_dir.mkdir(exist_ok=True)

    movidos = 0
    for csv_viejo in CARPETA_EXPORTS.glob("*.csv"):
        destino = archivo_dir / csv_viejo.name
        shutil.move(str(csv_viejo), str(destino))
        movidos += 1

    if movidos == 0:
        print("  No hay CSVs en exports/ para archivar.")
    else:
        print(f"  Archivados {movidos} CSVs a exports/archivo/")


def restaurar_backup():
    """Reto B: restaura datos/gastos.json y datos/log.txt desde un ZIP."""
    backups = sorted(CARPETA_BACKUPS.glob("backup_*.zip"))
    if not backups:
        print("  No hay backups disponibles.")
        return

    print("\n  --- Backups disponibles ---")
    for i, ruta in enumerate(backups, start=1):
        print(f"  {i}. {ruta.name}")

    try:
        eleccion = int(input("  Número del backup a restaurar: "))
        if eleccion < 1:
            raise IndexError  # evita que 0 o negativos tomen backups del final
        elegido = backups[eleccion - 1]
    except (ValueError, IndexError):
        print("  Opción no válida.")
        return

    # Antes de sobreescribir, guardamos una copia de seguridad con shutil.copy
    for archivo in (ARCHIVO_JSON, ARCHIVO_LOG):
        if archivo.exists():
            shutil.copy(archivo, archivo.with_name(archivo.name + ".antes_de_restaurar"))

    restaurados = 0
    with zipfile.ZipFile(elegido, "r") as zf:
        for nombre in zf.namelist():
            if nombre in ("datos/gastos.json", "datos/log.txt"):
                zf.extract(nombre, RAIZ)
                restaurados += 1

    print(f"  Restaurados {restaurados} archivo(s) desde {elegido.name}")


def menu():
    """Menú principal del Tracker de Gastos."""
    preparar_carpetas()

    while True:
        print("\n" + "=" * 45)
        print("  TRACKER DE GASTOS PERSONAL")
        print("=" * 45)
        print("  1. Agregar un gasto")
        print("  2. Ver todos los gastos")
        print("  3. Resumen por categoría")
        print("  4. Exportar mes actual a CSV")
        print("  5. Crear backup ZIP")
        print("  6. Salir")
        print("  7. Ver gastos del mes actual")
        print("  8. Restaurar desde un backup")
        print("  9. Eliminar un gasto")
        print("=" * 45)

        opcion = input("\n  Opción: ").strip()

        if opcion == "1":
            try:
                monto = float(input("  Monto: $"))
                categoria = input("  Categoría: ").strip().capitalize()
                descripcion = input("  Descripción: ").strip()
                agregar_gasto(monto, categoria, descripcion)
            except ValueError:
                print("  Error: el monto debe ser un número.")

        elif opcion == "2":
            mostrar_gastos(cargar_gastos())

        elif opcion == "3":
            resumen_por_categoria()

        elif opcion == "4":
            hoy = datetime.now()
            ruta = exportar_csv_mes(hoy.year, hoy.month)
            if ruta:
                print(f"  Total del mes según CSV: ${total_desde_csv(ruta):.2f}")

        elif opcion == "5":
            crear_backup()

        elif opcion == "6":
            print("  ¡Hasta luego!")
            break

        elif opcion == "7":
            hoy = datetime.now()
            mostrar_gastos(gastos_del_mes(hoy.year, hoy.month))

        elif opcion == "8":
            restaurar_backup()

        elif opcion == "9":
            try:
                eliminar_gasto(int(input("  Id del gasto a eliminar: #")))
            except ValueError:
                print("  Error: el id debe ser un número entero.")

        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    menu()
