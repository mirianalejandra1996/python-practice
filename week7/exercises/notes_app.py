ARCHIVO_NOTAS = "notas.txt"

def agregar_nota():
    nota = input("Escribe tu nota: ")
    with open(ARCHIVO_NOTAS, "a") as f:
        f.write(nota + "\n")
    print("Nota guardada.\n")

def ver_notas():
    try:
        with open(ARCHIVO_NOTAS, "r") as f:
            lineas = f.readlines()

        if not lineas:
            print("No hay notas guardadas.\n")
            return

        print("\n--- Tus notas ---")
        for i, linea in enumerate(lineas, start=1):
            print(f"{i}. {linea.strip()}")
        print()

    except FileNotFoundError:
        print("No hay notas guardadas todavía.\n")

while True:
    print("¿Qué quieres hacer?")
    print("1. Agregar nota")
    print("2. Ver notas")
    print("3. Salir")

    opcion = input("Elige (1/2/3): ").strip()

    if opcion == "1":
        agregar_nota()
    elif opcion == "2":
        ver_notas()
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intenta de nuevo.\n")