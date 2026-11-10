
import csv
import sys
import time
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from datetime import datetime

if len(sys.argv) != 2:
    print("Uso: python secuencial.py archivo.csv")
    sys.exit(1)

archivo = sys.argv[1]

inicio = time.perf_counter()

resultados = defaultdict(Decimal)
errores = 0

with open(archivo, "r", newline="", encoding="utf-8") as f:
    lector = csv.reader(f)

    for fila in lector:
        try:
            if not fila or fila[0] == "id":
                continue

            fecha_hora = datetime.strptime(
                fila[1], "%Y-%m-%d %H:%M:%S"
            )

            categoria = fila[3]
            cantidad = Decimal(fila[5])
            precio = Decimal(fila[6])

            ingreso = cantidad * precio

            clave = (fecha_hora.hour, categoria)
            resultados[clave] += ingreso

        except (IndexError, ValueError, InvalidOperation):
            errores += 1

fin = time.perf_counter()

print("RESULTADOS DEL PROCESAMIENTO SECUENCIAL")
print("-" * 55)
print("Hora | Categoría | Ingreso total")

for (hora, categoria), total in sorted(resultados.items()):
    print(f"{hora:02d} | {categoria} | {total:.2f}")

print("-" * 55)
print(f"Grupos obtenidos: {len(resultados)}")
print(f"Registros incorrectos: {errores}")
print(f"Tiempo de ejecución: {fin - inicio:.4f} segundos")
