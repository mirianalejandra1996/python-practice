# menu.py
def mostrar_menu():
    print("\n=== Mi Programa ===")
    print("1. Saludar")
    print("2. Calcular")
    print("3. Salir")
    return input("Elige una opción: ")

while True:
    opcion = mostrar_menu()

    if opcion == "1":
        nombre = input("Tu nombre: ")
        print(f"¡Hola, {nombre}!")
    elif opcion == "2":
        num = float(input("Un número: "))
        print(f"El doble es {num * 2}")
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida.")