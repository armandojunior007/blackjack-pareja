
def mostrar_carta(carta):
    return f'{carta["valor"]} de {carta["palo"]}'


def mostrar_mano(nombre, mano, puntuacion):
    print(f"\n--- {nombre} ---")

    for carta in mano:
        print(mostrar_carta(carta))

    print(f"Puntuación: {puntuacion}")


def mostrar_estado(juego, ocultar_crupier=False):
    print("\n" + "=" * 35)
    print("         BLACKJACK")
    print("=" * 35)

    if ocultar_crupier and not juego.terminado:
        print("\n--- CRUPIER ---")
        print(mostrar_carta(juego.crupier[0]))
        print("Segunda carta: OCULTA")
    else:
        mostrar_mano(
            "CRUPIER",
            juego.crupier,
            juego.obtener_puntuacion_crupier()
        )

    mostrar_mano(
        "JUGADOR",
        juego.jugador,
        juego.obtener_puntuacion_jugador()
    )

    print("=" * 35)


def pedir_accion():
    print("\n¿Qué quieres hacer?")
    print("1. Pedir carta")
    print("2. Plantarse")

    while True:
        opcion = input("Selecciona una opción (1 o 2): ").strip()

        if opcion in ["1", "2"]:
            return opcion

        print("Opción incorrecta. Inténtalo de nuevo.")


def mostrar_resultado(juego):
    mostrar_estado(juego)

    print("\n" + juego.resultado)
    print("\nFin de la partida.")
