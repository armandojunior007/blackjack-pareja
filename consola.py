"""Versión por consola del Blackjack.

Es la primera interfaz del proyecto. Se mantiene para poder jugar sin
ventana con: python main.py --consola
"""

from juego import JuegoBlackjack
from historial import guardar_resultado, mostrar_estadisticas


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


def jugar():
    print("\n¡Bienvenido al BLACKJACK!")
    print("El objetivo es conseguir 21 puntos sin pasarse.")

    juego = JuegoBlackjack()

    mostrar_estado(juego, ocultar_crupier=True)

    while not juego.terminado:

        opcion = pedir_accion()

        if opcion == "1":
            juego.pedir_carta()

            if not juego.terminado:
                mostrar_estado(juego, ocultar_crupier=True)

        elif opcion == "2":
            juego.plantarse()

    mostrar_resultado(juego)

    # Guardar el resultado de la partida
    guardar_resultado(juego.resultado)

    # Mostrar las estadísticas acumuladas
    mostrar_estadisticas()


def jugar_en_consola():
    """Juega partidas por consola hasta que el jugador quiera salir."""
    while True:
        jugar()

        otra = input("\n¿Quieres jugar otra partida? (s/n): ").lower().strip()

        if otra != "s":
            print("\n¡Gracias por jugar al Blackjack!")
            break
