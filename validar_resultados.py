
import csv
from decimal import Decimal
from collections import defaultdict

archivo_csv = "ventas_125054548.csv"
archivo_hadoop = "hadoop_resultados.txt"

# Leer resultados de Hadoop
resultados_hadoop = {}

with open(archivo_hadoop, "r", encoding="utf-8") as f:
    for linea in f:
        clave, valor = linea.strip().split("\t")
        resultados_hadoop[clave] = Decimal(valor)

# Calcular nuevamente los resultados desde el CSV
resultados_secuencial = defaultdict(Decimal)

with open(archivo_csv, "r", newline="", encoding="utf-8") as f:
    lector = csv.reader(f)

    for fila in lector:
        if not fila or fila[0] == "id":
            continue

        hora = fila[1][11:13]
        categoria = fila[3]
        cantidad = Decimal(fila[5])
        precio = Decimal(fila[6])

        clave = f"{hora}|{categoria}"
        resultados_secuencial[clave] += cantidad * precio

# Comparar ambos métodos
diferencias = []

for clave, total in resultados_secuencial.items():
    total_hadoop = resultados_hadoop.get(clave)

    if total_hadoop != total:
        diferencias.append(
            (clave, total, total_hadoop)
        )

print("VALIDACION DE RESULTADOS")
print("-" * 40)
print(f"Grupos secuenciales: {len(resultados_secuencial)}")
print(f"Grupos Hadoop: {len(resultados_hadoop)}")
print(f"Diferencias encontradas: {len(diferencias)}")

if not diferencias and len(resultados_hadoop) == len(resultados_secuencial):
    print("RESULTADO: AMBOS METODOS COINCIDEN")
else:
    print("RESULTADO: EXISTEN DIFERENCIAS")
    for diferencia in diferencias[:10]:
        print(diferencia)
