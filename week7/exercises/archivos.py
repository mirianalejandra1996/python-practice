ventas = []
ventas.append({"producto": "Café", "precio": 45})
ventas.append({"producto": "Pan", "precio": 30})
print(ventas)


with open("ventas.txt", "a") as f:
    f.write("Café,45\n")
    f.write("Pan,30\n")
    
    
archivo = open("ventas.txt", "r")