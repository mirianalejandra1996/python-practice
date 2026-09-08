print("Hola desde VS Code")

"""
Fase 2 — Mudanza a VS Code (15 min)
Repasa: cápsula 05 (transición a VS Code) y cápsula 06 (Python en la terminal).

Calculadora de Propinas — Semana 6
Versión 1: la calculadora de la Semana 1, ahora en VS Code
"""

class PorcentajeInvalidoError(Exception):
    pass


class PersonasInvalidoError(Exception):
    pass


class CuentaInvalidoError(Exception):
    pass


print("=" * 40)
print("    CALCULADORA DE PROPINAS")
print("=" * 40)


while True:
    try:
        cuenta = float(input("Monto de la cuenta: $"))

        if cuenta <= 0:
            raise CuentaInvalidoError(
                f"La cuenta debe ser > 0. Recibido: ${cuenta}"
            )

        porcentaje = int(input("Porcentaje de propina (15, 18, 20): "))

        personas = int(input("Personas: "))

        if porcentaje < 1 or porcentaje > 100:
            raise PorcentajeInvalidoError(
                f"El porcentaje debe estar entre 1 y 100. Recibido: {porcentaje}"
            )

        if personas <= 0:
            raise PersonasInvalidoError(
                f"El número de personas debe ser > 0. Recibido: {personas}"
            )

    except ValueError:
        print("Error: ingresa solo números válidos. Intenta de nuevo.\n")
        continue

    except (CuentaInvalidoError, PorcentajeInvalidoError, PersonasInvalidoError) as e:
        print(f"Error: {e}\n")
        continue

    except KeyboardInterrupt:
        print("\nCancelado por el usuario.")
        break

    else:
        # Calculamos la propina
        propina = cuenta * (porcentaje / 100)

        # Calculamos el total de la cuenta
        total = cuenta + propina

        # Calculamos cuánto debe pagar cada persona
        por_persona = total / personas

        print(f"\nPropina:        ${propina:.2f}")
        print(f"Total:          ${total:.2f}")
        print(f"Por persona:    ${por_persona:.2f}")

        # Guardamos el resultado en un archivo
        with open("ultimo_resultado.txt", "w") as f:
            f.write(f"Cuenta: ${cuenta:.2f}\n")
            f.write(f"Propina: ${propina:.2f}\n")
            f.write(f"Total: ${total:.2f}\n")
            f.write(f"Por persona: ${por_persona:.2f}\n")

        print("Resultado guardado en ultimo_resultado.txt")

        break


print("\nGracias por usar la calculadora.")
