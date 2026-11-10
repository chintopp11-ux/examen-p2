
import sys
from decimal import Decimal, InvalidOperation

clave_actual = None
total = Decimal("0")

for linea in sys.stdin:
    try:
        clave, valor = linea.strip().split("\t")
        ingreso = Decimal(valor)

        if clave == clave_actual:
            total += ingreso
        else:
            if clave_actual is not None:
                print(f"{clave_actual}\t{total:.2f}")

            clave_actual = clave
            total = ingreso

    except (ValueError, InvalidOperation):
        continue

# Imprimir el último grupo
if clave_actual is not None:
    print(f"{clave_actual}\t{total:.2f}")
