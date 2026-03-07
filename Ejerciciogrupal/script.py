"""
script.py
---------
Automatiza la actualización del sistema en distribuciones basadas en Debian/Ubuntu.
Ejecuta tres comandos apt-get en secuencia: update, upgrade y dist-upgrade.
Si algún paso falla, el script se detiene y reporta el error.
"""

import subprocess


def update_environment():
    """
    Ejecuta los tres pasos estándar de actualización del sistema:

    1. apt-get update     — Refresca la lista de paquetes disponibles desde los repositorios.
    2. apt-get upgrade    — Instala las versiones más nuevas de los paquetes ya instalados.
    3. apt-get dist-upgrade — Como upgrade, pero también resuelve cambios de dependencias
                             (puede instalar o eliminar paquetes si es necesario).

    Si un paso falla (código de salida distinto de 0), se lanza CalledProcessError,
    se imprime el error y se interrumpe la secuencia con break.
    """

    # Lista de comandos a ejecutar en orden. Cada comando es una lista de strings
    # para evitar inyección de shell (más seguro que pasar un string a shell=True).
    commands = [
        ["sudo", "apt-get", "update"],
        ["sudo", "apt-get", "upgrade", "-y"],       # -y: responde "sí" automáticamente
        ["sudo", "apt-get", "dist-upgrade", "-y"]   # -y: responde "sí" automáticamente
    ]

    # enumerate(commands, 1) entrega pares (índice, comando) con índice iniciando en 1
    for i, cmd in enumerate(commands, 1):
        print(f"--- Ejecutando paso {i}: {cmd} ---")

        try:
            # check=True hace que subprocess lance una excepción si el comando falla
            subprocess.run(cmd, check=True)
            print(f"✅ Paso {i} completado con éxito.\n")
        except subprocess.CalledProcessError as e:
            # El comando retornó un código de salida distinto de 0
            print(f"❌ Error en el paso {i} ({cmd}): {e}")
            break  # Detiene el loop; no tiene sentido continuar si un paso falló


# Punto de entrada: se ejecuta solo cuando el script se llama directamente
update_environment()