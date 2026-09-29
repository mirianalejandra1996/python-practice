with open("poema.txt", "w") as f:
    f.write("En un lugar de la Mancha\n")
    f.write("de cuyo nombre no quiero acordarme\n")
    f.write("\n")
    f.write("no ha mucho tiempo que vivía\n")
    f.write("un hidalgo de los de lanza en astillero\n")
    f.write("\n")
    f.write("adarga antigua, rocín flaco\n")
    f.write("y galgo corredor\n")

with open("poema.txt", "r") as f:
    lineas = f.readlines()

total_lineas = len(lineas)
# print(lineas)
no_vacias = sum(1 for linea in lineas if linea.strip())
total_caracteres = sum(len(linea) for linea in lineas)

print(f"Total de líneas: {total_lineas}")
print(f"Líneas no vacías: {no_vacias}")
print(f"Total de caracteres: {total_caracteres}")