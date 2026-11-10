
import sys
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation

lector = csv.reader(sys.stdin)

for fila in lector:
    try:
        # Ignorar encabezado
        if not fila or fila[0] == "id":
            continue

        # Extraer datos necesarios
        fecha_hora = datetime.strptime(
            fila[1], "%Y-%m-%d %H:%M:%S"
        )
        categoria = fila[3]
        cantidad = Decimal(fila[5])
        precio = Decimal(fila[6])

        # Calcular ingreso de la venta
        ingreso = cantidad * precio

        # Crear clave: hora y categoría
        clave = f"{fecha_hora.hour:02d}|{categoria}"

        # Enviar clave e ingreso
        print(f"{clave}\t{ingreso:.2f}")

    except (IndexError, ValueError, InvalidOperation):
        # Ignorar registros incorrectos
        continue
