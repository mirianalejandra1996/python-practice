"""
Semana 7: Archivos y Formatos de Datos
Archivos JSON

CSV es genial para tablas, pero el mundo real necesita datos con estructura jerárquica:
configuraciones con secciones anidadas, respuestas de APIs con objetos dentro de objetos,
bases de datos locales con relaciones complejas. Para eso existe JSON.

JSON (JavaScript Object Notation) es el formato estándar de la web.
! En la Semana 9 lo vas a usar como base de datos para tu proyecto final.

! Ejecuta este script desde la carpeta json_files/ para que los .json se creen aquí:
!   cd week7/exercises/json_files
!   py practica_json.py
"""


# ============================================================================================

"""
¿Qué es JSON?
Un formato de texto independiente del lenguaje que se usa en prácticamente todos
los lenguajes de programación.

{
  "nombre": "Ana García",
  "edad": 28,
  "activo": true,
  "cursos": ["Python", "SQL", "Machine Learning"],
  "direccion": {
    "ciudad": "Ciudad de México",
    "codigo_postal": "06600"
  }
}

¿Por qué JSON es tan popular?
- Legible para humanos — puedes abrir un .json y entender los datos
- Independiente del lenguaje — Python, JavaScript, Java, Go... todos lo soportan
- Jerárquico — soporta datos anidados (objetos dentro de objetos)
- El estándar de las APIs — si consumes una API, recibes JSON
- Ligero — menos verboso que XML, más flexible que CSV


JSON vs diccionarios de Python

Característica      JSON                        Python dict
Booleanos           true / false                True / False
Nulo                null                        None
Claves              Solo strings (con "")       Cualquier inmutable
Comillas            Solo dobles "texto"         Simples o dobles
Trailing comma      No permitido                Permitido
Comentarios         No soportados               # comentarios

! La regla de oro: JSON es más estricto que Python. Si un diccionario funciona en
! Python, no necesariamente es JSON válido. Pero si algo es JSON válido, Python
! puede leerlo sin problema.
"""

# Esto es un diccionario de Python (válido), pero NO es JSON válido
persona = {
    'nombre': 'Ana',
    'activo': True,
    'habilidades': None,
}

# Su equivalente en JSON:
# {
#   "nombre": "Ana",
#   "activo": true,
#   "habilidades": null
# }


# ============================================================================================

"""
El módulo json
Viene en la biblioteca estándar — no necesitas instalar nada.

Función         Dirección   Origen → Destino
json.load()     Leer        Archivo → Python
json.loads()    Leer        String → Python
json.dump()     Escribir    Python → Archivo
json.dumps()    Escribir    Python → String

! Truco: la "s" al final significa string. Sin s = archivo, con s = string.
"""

import json
from pathlib import Path

# Creamos contactos.json para poder usarlo en el ejemplo de lectura
Path("contactos.json").write_text(
    """[
  {"nombre": "Ana", "telefono": "555-0001", "email": "ana@email.com"},
  {"nombre": "Carlos", "telefono": "555-0002", "email": "carlos@email.com"},
  {"nombre": "María", "telefono": "555-0003", "email": "maria@email.com"}
]
""",
    encoding="utf-8",
)


# ============================================================================================

"""
Leer archivos JSON
json.load() — de archivo a Python
"""

with open("contactos.json", "r", encoding="utf-8") as archivo:
    contactos = json.load(archivo)

print(type(contactos))
# <class 'list'>

print(contactos[0]["nombre"])
# Ana

for contacto in contactos:
    print(f"{contacto['nombre']}: {contacto['telefono']}")
# Ana: 555-0001
# Carlos: 555-0002
# María: 555-0003

"""
json.load() convierte automáticamente:
- Objetos JSON {}   → diccionarios Python dict
- Arrays JSON []    → listas Python list
- true/false        → True/False
- null              → None
- Números           → int o float
"""



# json.loads() — de string a Python (por ejemplo, la respuesta de una API)

texto_json = '{"nombre": "Ana", "edad": 28, "activo": true}'

datos = json.loads(texto_json)

print(datos["nombre"])
# Ana

print(datos["activo"])
# True (Python bool, no string)


# ============================================================================================

"""
Escribir archivos JSON
json.dump() — de Python a archivo
"""

contactos = [
    {"nombre": "Ana", "telefono": "555-0001", "email": "ana@email.com"},
    {"nombre": "Carlos", "telefono": "555-0002", "email": "carlos@email.com"},
]

with open("contactos.json", "w", encoding="utf-8") as archivo:
    json.dump(contactos, archivo)

# Esto crea el archivo, pero todo en una sola línea. Para hacerlo legible:

with open("contactos.json", "w", encoding="utf-8") as archivo:
    json.dump(contactos, archivo, indent=2, ensure_ascii=False)

"""
Parámetros importantes:

Parámetro           Qué hace                                    Ejemplo
indent=2            Agrega indentación (legibilidad)            Formato bonito
ensure_ascii=False  Permite caracteres especiales (ñ, é, á)     "año" en vez de "a\\u00f1o"
sort_keys=True      Ordena las claves alfabéticamente           Consistencia

! Siempre usa ensure_ascii=False cuando trabajes en español.
! Sin él, "María" se guarda como "Mar\\u00eda".
"""



# json.dumps() — de Python a string (útil para debugging, logging o enviar a una API)

datos = {"nombre": "María", "edad": 25, "ciudad": "Guadalajara"}

texto_json = json.dumps(datos, indent=2, ensure_ascii=False)
print(texto_json)
# {
#   "nombre": "María",
#   "edad": 25,
#   "ciudad": "Guadalajara"
# }


# ============================================================================================

"""
Ejemplo práctico: sistema de configuración
Lee, modifica y guarda un archivo de configuración.
"""

ARCHIVO_CONFIG = "config.json"

CONFIG_DEFAULT = {
    "idioma": "es",
    "tema": "oscuro",
    "fuente_tamano": 14,
    "notificaciones": True,
    "carpeta_descargas": "./descargas",
    "historial": {
        "guardar": True,
        "max_entradas": 100
    }
}


def cargar_config():
    """Carga la configuración. Si no existe, crea una con valores por defecto."""
    ruta = Path(ARCHIVO_CONFIG)

    if not ruta.exists():
        print("Archivo de configuración no encontrado. Creando con valores por defecto...")
        guardar_config(CONFIG_DEFAULT)
        return CONFIG_DEFAULT.copy()

    with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)

    print("Configuración cargada correctamente.")
    return config


def guardar_config(config):
    """Guarda la configuración en el archivo JSON."""
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("Configuración guardada.")


def mostrar_config(config):
    """Muestra la configuración actual."""
    print("\n--- Configuración actual ---")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("----------------------------\n")


config = cargar_config()
mostrar_config(config)

config["tema"] = "claro"
config["fuente_tamano"] = 16
config["historial"]["max_entradas"] = 200

print("Configuración modificada:")
mostrar_config(config)

guardar_config(config)

# La primera vez que ejecutas el script crea config.json con los valores por defecto.
# Las siguientes veces lo carga (ya con los valores modificados).


# ============================================================================================

"""
Ejemplo práctico: JSON como "base de datos"
Adelanto del patrón del proyecto CRUD de la Semana 9 (Crear, Leer, Actualizar, Eliminar).
"""

ARCHIVO_DB = "productos.json"


def cargar_datos():
    """Carga los datos del archivo JSON. Retorna lista vacía si no existe."""
    ruta = Path(ARCHIVO_DB)
    if not ruta.exists():
        return []

    with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_datos(datos):
    """Guarda la lista de datos en el archivo JSON."""
    with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def agregar_producto(nombre, precio, cantidad):
    """Agrega un nuevo producto a la base de datos."""
    productos = cargar_datos()

    nuevo = {
        "id": len(productos) + 1,
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }

    productos.append(nuevo)
    guardar_datos(productos)
    print(f"Producto '{nombre}' agregado con ID {nuevo['id']}")


def listar_productos():
    """Muestra todos los productos."""
    productos = cargar_datos()

    if not productos:
        print("No hay productos registrados.")
        return

    print(f"\n{'ID':<5} {'Nombre':<20} {'Precio':<10} {'Cantidad':<10}")
    print("-" * 45)
    for p in productos:
        print(f"{p['id']:<5} {p['nombre']:<20} ${p['precio']:<9.2f} {p['cantidad']:<10}")
    print()


# Borramos productos.json para que cada ejecución empiece desde cero
# (si no, los productos se agregan otra vez cada vez que corres el script)
Path(ARCHIVO_DB).unlink(missing_ok=True)

agregar_producto("Laptop", 15999.99, 5)
agregar_producto("Mouse", 299.50, 20)
agregar_producto("Teclado", 599.00, 15)

listar_productos()

"""
! Este patrón — cargar_datos() y guardar_datos() — es el corazón de tu proyecto
! final en la Semana 9. La app CRUD va a:
! - Leer datos de un archivo JSON al iniciar
! - Permitir crear, buscar, actualizar y eliminar registros
! - Guardar cambios de vuelta al JSON
! - Manejar errores si el archivo no existe o está corrupto
"""


# ============================================================================================
# TROUBLESHOOTING
# ============================================================================================

# Problema 1: json.JSONDecodeError (JSON mal formado)

texto_malo = "{'nombre': 'Ana'}"  # Comillas simples — NO es JSON válido

try:
    datos = json.loads(texto_malo)
except json.JSONDecodeError as e:
    print(f"Error: {e}")
# Expecting property name enclosed in double quotes

# Causa: JSON requiere comillas dobles. Si el string tiene comillas simples,
# trailing commas o comentarios, no es JSON válido.
# Solución: asegúrate de que el contenido sea JSON válido:

texto_bueno = '{"nombre": "Ana"}'
datos = json.loads(texto_bueno)
print(datos)

# Si lees de un archivo y sospechas que está corrupto:
try:
    with open("contactos.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error en el JSON: {e}")
    print("Verifica que el archivo tenga formato JSON válido.")



# Problema 2: TypeError — objeto no serializable

from datetime import datetime

datos = {
    "nombre": "Ana",
    "fecha": datetime.now(),
    "tags": {"python", "json"}  # set
}

try:
    json.dumps(datos)
except TypeError as e:
    print(f"Error: {e}")
# Object of type datetime is not JSON serializable

# Causa: JSON solo soporta strings, números, booleanos, null, listas y objetos.
# No puede serializar datetime, set, clases personalizadas, etc.
# Solución: convierte los tipos no soportados antes de serializar:

datos = {
    "nombre": "Ana",
    "fecha": datetime.now().isoformat(),  # Convertir a string ISO
    "tags": list({"python", "json"})      # Convertir set a lista
}

print(json.dumps(datos, indent=2, ensure_ascii=False))



# Problema 3: Caracteres especiales se guardan como códigos Unicode

datos = {"ciudad": "Monterrey", "país": "México"}

# SIN ensure_ascii=False
print(json.dumps(datos))
# {"ciudad": "Monterrey", "país": "México"}

# CON ensure_ascii=False
print(json.dumps(datos, ensure_ascii=False))
# {"ciudad": "Monterrey", "país": "México"}

# Causa: por defecto, json.dumps() escapa todos los caracteres no-ASCII.
# Solución: siempre usa ensure_ascii=False en español, y encoding="utf-8" al abrir archivos:

with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)


"""
Resumen

Concepto                Detalle
JSON                    Formato de texto estándar para datos estructurados
json.load(f)            Lee un archivo JSON → Python dict/list
json.loads(s)           Lee un string JSON → Python dict/list
json.dump(data, f)      Escribe Python → archivo JSON
json.dumps(data)        Escribe Python → string JSON
indent=2                Formato legible con indentación
ensure_ascii=False      Preserva caracteres como ñ, é, á
JSON vs dict            JSON es más estricto: solo "", true/false, null

! Lo esencial: json.load() para leer, json.dump() para escribir,
! ensure_ascii=False para español. Domina estos 3 y estás listo.

Recursos adicionales
- Documentación oficial — módulo json: https://docs.python.org/3/library/json.html
- JSON.org — especificación del formato: https://www.json.org/json-es.html
- Real Python — Working with JSON: https://realpython.com/python-json/
"""
