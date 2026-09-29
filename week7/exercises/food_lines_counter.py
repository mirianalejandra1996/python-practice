with open("mi_archivo.txt", "w") as f:
    f.write("Tacos\n")
    f.write("Sushi\n")
    f.write("Pizza\n")

with open("mi_archivo.txt", "r") as f:
    for i, linea in enumerate(f, start=1):
        print(f"Línea {i}: {linea.strip()}")