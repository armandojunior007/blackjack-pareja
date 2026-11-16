
import random

# Palos de la baraja
PALOS = ["Corazones", "Diamantes", "Treboles", "Picas"]

# Valores de las cartas
VALORES = {
    "As": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}


def crear_baraja():
    """Crea una baraja de 52 cartas."""
    baraja = []

    for palo in PALOS:
        for valor in VALORES:
            carta = {
                "valor": valor,
                "palo": palo,
                "puntos": VALORES[valor]
            }

            baraja.append(carta)

    random.shuffle(baraja)

    return baraja


def repartir_carta(baraja):
    """Reparte una carta de la baraja."""
    if len(baraja) > 0:
        return baraja.pop()

    return None
