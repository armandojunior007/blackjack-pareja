
from juego import JuegoBlackjack
from interfaz import mostrar_estado, pedir_accion, mostrar_resultado


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


def main():
    while True:
        jugar()

        otra = input("\n¿Quieres jugar otra partida? (s/n): ").lower().strip()

        if otra != "s":
            print("\n¡Gracias por jugar al Blackjack!")
            break


if __name__ == "__main__":
    main()
