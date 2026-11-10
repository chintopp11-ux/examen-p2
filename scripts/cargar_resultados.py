import requests
from decimal import Decimal
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent.parent / "hadoop_resultados.txt"
API_URL = "http://localhost:5000/resultados"

enviados = 0
errores = 0

with open(ARCHIVO, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        try:
            clave, valor = linea.strip().split("\t")
            hora, categoria = clave.split("|")

            datos = {
                "hora": int(hora),
                "categoria": categoria,
                "ingreso": float(Decimal(valor))
            }

            respuesta = requests.post(
                API_URL,
                json=datos,
                timeout=15
            )

            respuesta.raise_for_status()
            enviados += 1

        except Exception as error:
            errores += 1
            print(f"Error en línea: {linea.strip()} -> {error}")

print("CARGA FINALIZADA")
print("--------------------------")
print(f"Resultados enviados: {enviados}")
print(f"Errores: {errores}")