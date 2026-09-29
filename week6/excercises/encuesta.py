# encuesta.py
print("=== Encuesta rápida ===\n")

nombre = input("Tu nombre: ")
edad = input("Tu edad: ")
lenguaje = input("Tu lenguaje favorito: ")

print(f"\n--- Resultados ---")
print(f"Nombre: {nombre}")
print(f"Edad: {edad}")
print(f"Lenguaje favorito: {lenguaje}")

if lenguaje.lower() == "python":
    print("¡Excelente elección!")
else:
    print(f"{lenguaje} está bien, pero Python es mejor 😄")