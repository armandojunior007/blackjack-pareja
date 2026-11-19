
import json
import os

ARCHIVO = "historial.json"


def cargar_historial():
    """Carga las estadísticas guardadas."""

    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return {
        "victorias": 0,
        "derrotas": 0,
        "empates": 0,
        "partidas": []
    }


def guardar_resultado(resultado):
    """Guarda el resultado de una partida."""

    historial = cargar_historial()

    if "Empate" in resultado:
        historial["empates"] += 1
        tipo = "Empate"

    elif "Has ganado" in resultado:
        historial["victorias"] += 1
        tipo = "Victoria"

    else:
        historial["derrotas"] += 1
        tipo = "Derrota"

    historial["partidas"].append(tipo)

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)


def mostrar_estadisticas():
    """Muestra las estadísticas acumuladas."""

    historial = cargar_historial()

    print("\n========== ESTADÍSTICAS ==========")
    print(f"Victorias: {historial['victorias']}")
    print(f"Derrotas: {historial['derrotas']}")
    print(f"Empates: {historial['empates']}")
    print(f"Total de partidas: {len(historial['partidas'])}")
    print("==================================")
