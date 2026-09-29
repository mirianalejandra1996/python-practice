"""
Ejercicios — Archivos JSON

! Ejecuta este script desde la carpeta json_files/ para que los .json se creen aquí:
!   cd week7/exercises/json_files
!   py ejercicios_json.py
"""

import json
from pathlib import Path


# ============================================================================================
# Ejercicio 1: Crear y leer contactos (Fácil)
# 1. Define una lista con 3 contactos (nombre, teléfono y email)
# 2. Guárdala en contactos.json con formato legible
# 3. Lee el archivo de vuelta e imprime cada contacto
# ============================================================================================

contactos = [
    {"nombre": "Ana", "telefono": "555-0001", "email": "ana@email.com"},
    {"nombre": "Carlos", "telefono": "555-0002", "email": "carlos@email.com"},
    {"nombre": "María", "telefono": "555-0003", "email": "maria@email.com"},
]

with open("contactos.json", "w", encoding="utf-8") as f:
    json.dump(contactos, f, indent=2, ensure_ascii=False)

with open("contactos.json", "r", encoding="utf-8") as f:
    contactos_leidos = json.load(f)

print("Contactos:")
for contacto in contactos_leidos:
    print(f"  {contacto['nombre']} | {contacto['telefono']} | {contacto['email']}")


# ============================================================================================
# Ejercicio 2: Agregar entrada a un JSON existente (Fácil)
# Lee tareas.json, agrega una nueva tarea y guárdalo de vuelta.
# ============================================================================================

# Creamos tareas.json con su contenido inicial (así cada ejecución empieza igual)
tareas_iniciales = [
    {"titulo": "Estudiar JSON", "completada": False},
    {"titulo": "Hacer ejercicios", "completada": False},
]

with open("tareas.json", "w", encoding="utf-8") as f:
    json.dump(tareas_iniciales, f, indent=2, ensure_ascii=False)

with open("tareas.json", "r", encoding="utf-8") as f:
    tareas = json.load(f)

tareas.append({"titulo": "Repasar CSV", "completada": False})

with open("tareas.json", "w", encoding="utf-8") as f:
    json.dump(tareas, f, indent=2, ensure_ascii=False)

print("\nTareas:")
for tarea in tareas:
    marca = "x" if tarea["completada"] else " "
    print(f"  [{marca}] {tarea['titulo']}")


# ============================================================================================
# Ejercicio 3: Agenda con persistencia JSON (Medio)
# 1. Al iniciar, carga contactos de agenda.json (si existe)
# 2. Permite agregar nuevos contactos
# 3. Permite listar todos los contactos
# 4. Guarda automáticamente después de cada cambio
# ============================================================================================

ARCHIVO_AGENDA = "agenda.json"


def cargar_agenda():
    """Carga la agenda. Retorna lista vacía si el archivo no existe."""
    if not Path(ARCHIVO_AGENDA).exists():
        return []

    with open(ARCHIVO_AGENDA, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_agenda(agenda):
    """Guarda la agenda en el archivo JSON."""
    with open(ARCHIVO_AGENDA, "w", encoding="utf-8") as f:
        json.dump(agenda, f, indent=2, ensure_ascii=False)


def agregar_contacto(agenda, nombre, telefono):
    """Agrega un contacto y guarda automáticamente."""
    for contacto in agenda:
        if contacto["nombre"] == nombre:
            print(f"'{nombre}' ya está en la agenda.")
            return

    agenda.append({"nombre": nombre, "telefono": telefono})
    guardar_agenda(agenda)
    print(f"'{nombre}' agregado a la agenda.")


def listar_contactos(agenda):
    """Muestra todos los contactos."""
    if not agenda:
        print("La agenda está vacía.")
        return

    for contacto in agenda:
        print(f"  {contacto['nombre']}: {contacto['telefono']}")


def menu():
    """Menú interactivo de la agenda."""
    agenda = cargar_agenda()

    while True:
        print("\n1. Agregar contacto")
        print("2. Listar contactos")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            agregar_contacto(agenda, nombre, telefono)
        elif opcion == "2":
            listar_contactos(agenda)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")


print("\nAgenda:")
agenda = cargar_agenda()
agregar_contacto(agenda, "Lucía", "555-1001")
agregar_contacto(agenda, "Roberto", "555-1002")
listar_contactos(agenda)

# Para usar la agenda de forma interactiva, descomenta esta línea:
# menu()


# ============================================================================================
# Ejercicio 4: Sistema de configuración robusto (Medio)
# 1. Lee un archivo de configuración JSON
# 2. Si no existe, créalo con valores por defecto
# 3. Permite modificar una configuración por clave
# 4. Guarda los cambios
# ============================================================================================

# Usamos configuracion.json para no chocar con el config.json de practica_json.py
ARCHIVO_CONFIGURACION = "configuracion.json"

CONFIGURACION_DEFAULT = {
    "idioma": "es",
    "tema": "oscuro",
    "fuente_tamano": 14,
    "notificaciones": True,
}


def cargar_configuracion():
    """Carga la configuración. Si no existe, la crea con valores por defecto."""
    if not Path(ARCHIVO_CONFIGURACION).exists():
        print("Configuración no encontrada. Creando con valores por defecto...")
        guardar_configuracion(CONFIGURACION_DEFAULT)
        return CONFIGURACION_DEFAULT.copy()

    with open(ARCHIVO_CONFIGURACION, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_configuracion(config):
    """Guarda la configuración en el archivo JSON."""
    with open(ARCHIVO_CONFIGURACION, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def modificar_configuracion(clave, valor):
    """Cambia el valor de una clave existente y guarda."""
    config = cargar_configuracion()

    if clave not in config:
        print(f"La clave '{clave}' no existe. Claves válidas: {list(config)}")
        return

    config[clave] = valor
    guardar_configuracion(config)
    print(f"'{clave}' actualizado a {valor!r}.")


print("\nConfiguración:")
modificar_configuracion("tema", "claro")
modificar_configuracion("fuente_tamano", 18)
modificar_configuracion("color", "azul")  # clave que no existe
print(json.dumps(cargar_configuracion(), indent=2, ensure_ascii=False))


# ============================================================================================
# Ejercicio 5: Procesar datos anidados (Medio)
# Lee escuela.json, calcula el promedio por estudiante y escribe resumen.json.
# ============================================================================================

escuela = {
    "grupo": "Python-2025",
    "estudiantes": [
        {"nombre": "Ana", "calificaciones": {"python": 95, "sql": 88, "git": 92}},
        {"nombre": "Carlos", "calificaciones": {"python": 78, "sql": 82, "git": 85}},
        {"nombre": "María", "calificaciones": {"python": 91, "sql": 95, "git": 89}},
        {"nombre": "Luis", "calificaciones": {"python": 85, "sql": 70, "git": 78}},
    ],
}

with open("escuela.json", "w", encoding="utf-8") as f:
    json.dump(escuela, f, indent=2, ensure_ascii=False)

with open("escuela.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

promedios = []
for estudiante in datos["estudiantes"]:
    notas = estudiante["calificaciones"].values()
    promedio = round(sum(notas) / len(notas), 1)
    promedios.append({"nombre": estudiante["nombre"], "promedio": promedio})

resumen = {
    "grupo": datos["grupo"],
    "promedios": promedios,
}

with open("resumen.json", "w", encoding="utf-8") as f:
    json.dump(resumen, f, indent=2, ensure_ascii=False)

print("\nArchivo resumen.json generado:")
print(json.dumps(resumen, indent=2, ensure_ascii=False))
