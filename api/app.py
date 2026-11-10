
import os
import time
from pathlib import Path
from decimal import Decimal, InvalidOperation

from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Archivos compartidos con el contenedor Hadoop
ARCHIVO_HADOOP = Path(
    "/tmp/examen/salida_automatico/part-00000"
)
MARCADOR_HADOOP = Path("/tmp/examen/hadoop_listo")


def conectar_bd():
    for intento in range(10):
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                database=os.getenv("DB_NAME", "examen"),
                user=os.getenv("DB_USER", "admin"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT", "5432")
            )
        except psycopg2.OperationalError:
            time.sleep(3)

    raise Exception("No fue posible conectar con PostgreSQL")


def crear_tabla():
    conexion = conectar_bd()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultados (
                    id SERIAL PRIMARY KEY,
                    hora INTEGER NOT NULL,
                    categoria VARCHAR(100) NOT NULL,
                    ingreso NUMERIC(18,2) NOT NULL,
                    UNIQUE (hora, categoria)
                )
            """)

        conexion.commit()
    finally:
        conexion.close()


def esperar_hadoop():
    print("Esperando a que Hadoop termine...")

    limite = time.time() + 900

    while time.time() < limite:
        if MARCADOR_HADOOP.exists() and ARCHIVO_HADOOP.exists():
            print("Resultados de Hadoop disponibles.")
            return

        time.sleep(5)

    raise TimeoutError(
        "Hadoop no terminó dentro del tiempo esperado."
    )


def cargar_resultados_hadoop():
    esperar_hadoop()

    resultados = []

    with open(ARCHIVO_HADOOP, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            try:
                clave, valor = linea.strip().split("\t")
                hora, categoria = clave.split("|", 1)

                hora = int(hora)
                ingreso = Decimal(valor)

                if not 0 <= hora <= 23 or not categoria:
                    raise ValueError("Dato fuera de rango")

                resultados.append((hora, categoria, ingreso))

            except (ValueError, InvalidOperation):
                raise ValueError(
                    f"Resultado Hadoop inválido: {linea.strip()}"
                )

    if len(resultados) != 240:
        raise ValueError(
            f"Se esperaban 240 resultados y se encontraron {len(resultados)}."
        )

    conexion = conectar_bd()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM resultados")

            cursor.executemany("""
                INSERT INTO resultados (hora, categoria, ingreso)
                VALUES (%s, %s, %s)
                ON CONFLICT (hora, categoria)
                DO UPDATE SET ingreso = EXCLUDED.ingreso
            """, resultados)

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()

    print(f"Se cargaron {len(resultados)} resultados en PostgreSQL.")


@app.route("/health", methods=["GET"])
def health():
    try:
        conexion = conectar_bd()
        conexion.close()

        return jsonify({
            "estado": "correcto",
            "base_datos": "conectada"
        }), 200

    except Exception as error:
        return jsonify({
            "estado": "error",
            "detalle": str(error)
        }), 500


@app.route("/resultados", methods=["GET"])
def consultar_resultados():
    conexion = conectar_bd()

    try:
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT hora, categoria, ingreso
                FROM resultados
                ORDER BY hora, categoria
            """)

            datos = cursor.fetchall()

        return jsonify(datos), 200

    finally:
        conexion.close()


@app.route("/resultados", methods=["POST"])
def guardar_resultado():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Se requiere un objeto JSON"
        }), 400

    try:
        hora = int(datos["hora"])
        categoria = str(datos["categoria"]).strip()
        ingreso = Decimal(str(datos["ingreso"]))

        if (
            not 0 <= hora <= 23
            or not categoria
            or not ingreso.is_finite()
            or ingreso < 0
        ):
            raise ValueError("Datos fuera de rango")

        conexion = conectar_bd()

        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO resultados (hora, categoria, ingreso)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (hora, categoria)
                    DO UPDATE SET ingreso = EXCLUDED.ingreso
                """, (hora, categoria, ingreso))

            conexion.commit()

        finally:
            conexion.close()

        return jsonify({
            "mensaje": "Resultado guardado correctamente"
        }), 201

    except (KeyError, ValueError, TypeError, InvalidOperation):
        return jsonify({"error": "Datos inválidos"}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    crear_tabla()
    cargar_resultados_hadoop()
    app.run(host="0.0.0.0", port=5000)
