import sys

from consola import jugar_en_consola


def main():
    """Abre la ventana del juego, o la consola si se pide con --consola."""
    if "--consola" in sys.argv:
        jugar_en_consola()
        return

    try:
        from interfaz import iniciar_interfaz
    except ImportError:
        print("No está disponible tkinter, así que se abre la versión por consola.")
        jugar_en_consola()
        return

    iniciar_interfaz()


if __name__ == "__main__":
    main()
