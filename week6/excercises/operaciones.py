# operaciones.py — esto es un módulo
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b

if __name__ == "__main__":
    print("Probando operaciones:")
    print(f"5 + 3 = {sumar(5, 3)}")
    print(f"10 - 4 = {restar(10, 4)}")