def calcular_descuento(precio, porcentaje):
    descuento = precio * (porcentaje / 100)
    precio_final = precio - descuento
    return precio_final

def aplicar_descuentos(productos):
    resultados = []
    for nombre, precio, descuento in productos:
        precio_final = calcular_descuento(precio, descuento)
        resultados.append({
            "nombre": nombre,
            "original": precio,
            "final": precio_final
        })
    return resultados

productos = [
    ("Laptop", 15000, 10),
    ("Mouse", 500, 15),
    ("Teclado", 800, 20),
]

resultados = aplicar_descuentos(productos)
for r in resultados:
    print(f"{r['nombre']}: ${r['original']} → ${r['final']}")