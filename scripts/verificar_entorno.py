
import os
import subprocess

ARCHIVOS_NECESARIOS = [
    ".env",
    "docker-compose.yml",
    "generar_dataset.py",
    "mapreduce/mapper.py",
    "mapreduce/reducer.py",
    "api/app.py",
    "ventas_125054548.csv"
]

def verificar_archivos():
    print("=== VERIFICACION DE ARCHIVOS ===")
    correcto = True

    for archivo in ARCHIVOS_NECESARIOS:
        if os.path.exists(archivo):
            print(f"[OK] {archivo}")
        else:
            print(f"[FALTA] {archivo}")
            correcto = False

    return correcto

def verificar_docker():
    print("=== VERIFICACION DE DOCKER ===")

    try:
        resultado = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[OK] {resultado.stdout.strip()}")
        return True

    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[ERROR] Docker no esta disponible.")
        return False

def main():
    print("VERIFICACION DEL ENTORNO DEL PROYECTO")

    archivos_ok = verificar_archivos()
    docker_ok = verificar_docker()

    print("=== RESULTADO FINAL ===")

    if archivos_ok and docker_ok:
        print("ENTORNO LISTO PARA EJECUTAR EL PROYECTO.")
    else:
        print("FALTAN REQUISITOS. REVISA LOS MENSAJES ANTERIORES.")

if __name__ == "__main__":
    main()
