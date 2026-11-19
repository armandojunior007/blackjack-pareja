

from cartas import crear_baraja, repartir_carta


class JuegoBlackjack:

    def __init__(self):
        self.baraja = crear_baraja()
        self.jugador = []
        self.crupier = []
        self.terminado = False
        self.resultado = ""

        # Repartir dos cartas a cada participante
        for i in range(2):
            self.jugador.append(repartir_carta(self.baraja))
            self.crupier.append(repartir_carta(self.baraja))

        # Comprobar si alguien tiene Blackjack inicial
        self.comprobar_blackjack_inicial()

    def calcular_puntuacion(self, mano):
        """Calcula los puntos de una mano."""
        puntuacion = sum(carta["puntos"] for carta in mano)

        # El As vale 11 o 1 según convenga
        ases = sum(1 for carta in mano if carta["valor"] == "As")

        while puntuacion > 21 and ases > 0:
            puntuacion -= 10
            ases -= 1

        return puntuacion

    def es_blackjack(self, mano):
        """Comprueba si una mano tiene Blackjack natural."""
        return (
            len(mano) == 2
            and self.calcular_puntuacion(mano) == 21
        )

    def comprobar_blackjack_inicial(self):
        """Comprueba el Blackjack de las dos primeras cartas."""
        jugador_blackjack = self.es_blackjack(self.jugador)
        crupier_blackjack = self.es_blackjack(self.crupier)

        if jugador_blackjack and crupier_blackjack:
            self.terminado = True
            self.resultado = "¡Ambos tienen Blackjack! ¡Empate!"

        elif jugador_blackjack:
            self.terminado = True
            self.resultado = "¡Blackjack natural! ¡Has ganado!"

        elif crupier_blackjack:
            self.terminado = True
            self.resultado = "El crupier tiene Blackjack. Has perdido."

    def pedir_carta(self):
        """El jugador pide una carta."""
        if not self.terminado:
            carta = repartir_carta(self.baraja)

            if carta is not None:
                self.jugador.append(carta)

            if self.calcular_puntuacion(self.jugador) > 21:
                self.terminado = True
                self.resultado = "Te has pasado de 21. Gana el crupier."

    def plantarse(self):
        """El jugador deja de pedir cartas."""
        if not self.terminado:
            self.turno_crupier()
    
    def turno_crupier(self):
        """El crupier juega automáticamente."""
        while self.calcular_puntuacion(self.crupier) < 17:
            carta = repartir_carta(self.baraja)

            if carta is not None:
                self.crupier.append(carta)
            else:
                break

        self.terminado = True
        self.determinar_ganador()

    def determinar_ganador(self):
        """Compara las puntuaciones y determina el ganador."""
        puntos_jugador = self.calcular_puntuacion(self.jugador)
        puntos_crupier = self.calcular_puntuacion(self.crupier)

        if puntos_crupier > 21:
            self.resultado = "¡El crupier se ha pasado! ¡Has ganado!"

        elif puntos_jugador > puntos_crupier:
            self.resultado = "¡Enhorabuena! ¡Has ganado!"

        elif puntos_jugador < puntos_crupier:
            self.resultado = "Ha ganado el crupier."

        else:
            self.resultado = "¡Empate!"

    def obtener_puntuacion_jugador(self):
        return self.calcular_puntuacion(self.jugador)

    def obtener_puntuacion_crupier(self):
        return self.calcular_puntuacion(self.crupier)
