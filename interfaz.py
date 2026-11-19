"""Interfaz gráfica del Blackjack hecha con tkinter.

Dibuja la mesa, recoge lo que hace el jugador (botones y teclado) y lleva
el flujo de cada partida. Las reglas están en juego.py: desde aquí solo se
llama a sus métodos y se enseña el resultado.
"""

import tkinter as tk
from tkinter import messagebox

from juego import JuegoBlackjack


# Medidas de la mesa, en píxeles para una pantalla al 100 %
ANCHO_MESA = 900
ALTO_MESA = 580
ANCHO_CARTA = 90
ALTO_CARTA = 130
HUECO_CARTAS = 14
Y_CARTAS_CRUPIER = 128
Y_MENSAJE = 300
Y_CARTAS_JUGADOR = 345

# Colores
VERDE_MESA = "#0b6138"
VERDE_OSCURO = "#06401f"
VERDE_APAGADO = "#3d6b4f"
SOMBRA = "#04331a"
DORADO = "#d4af37"
DORADO_CLARO = "#f0cf60"
BLANCO = "#ffffff"
GRIS_CLARO = "#b9d8c3"
ROJO_CLARO = "#ff8a80"
CARTA = "#fbfbf6"
BORDE_CARTA = "#9e9e9e"
ROJO = "#c62828"
NEGRO = "#1d1d1d"
AZUL_REVERSO = "#1c3f94"
AZUL_ROMBOS = "#3a62c4"

FUENTE = "Arial"

# Tiempos de las animaciones, en milisegundos
PAUSA_REPARTO = 350
PAUSA_CRUPIER = 700

SIMBOLOS = {
    "Corazones": "♥",
    "Diamantes": "♦",
    "Treboles": "♣",
    "Picas": "♠"
}

PALOS_ROJOS = ("Corazones", "Diamantes")

# Estados del flujo de una partida:
#   repartiendo -> jugador -> crupier -> fin -> (nueva partida) repartiendo
REPARTIENDO = "repartiendo"
TURNO_JUGADOR = "jugador"
TURNO_CRUPIER = "crupier"
FIN = "fin"


def rectangulo_redondeado(lienzo, x1, y1, x2, y2, radio, **opciones):
    """Dibuja un rectángulo con las esquinas redondeadas."""
    puntos = [
        x1 + radio, y1, x1 + radio, y1,
        x2 - radio, y1, x2 - radio, y1,
        x2, y1,
        x2, y1 + radio, x2, y1 + radio,
        x2, y2 - radio, x2, y2 - radio,
        x2, y2,
        x2 - radio, y2, x2 - radio, y2,
        x1 + radio, y2, x1 + radio, y2,
        x1, y2,
        x1, y2 - radio, x1, y2 - radio,
        x1, y1 + radio, x1, y1 + radio,
        x1, y1
    ]

    return lienzo.create_polygon(puntos, smooth=True, **opciones)


def clasificar_resultado(texto):
    """Dice si el resultado de juego.py es una partida ganada, perdida o empatada."""
    texto = texto.lower()

    if "empate" in texto:
        return "empates"

    if "has ganado" in texto:
        return "ganadas"

    return "perdidas"


class InterfazBlackjack:
    """Ventana del juego: mesa, botones, teclado y flujo de la partida."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Blackjack")
        self.raiz.configure(bg=VERDE_OSCURO)
        self.raiz.resizable(False, False)

        # En pantallas con zoom (125 %, 150 %...) la mesa crece en proporción
        self.escala = max(1.0, raiz.winfo_fpixels("1i") / 96)

        self.juego = None
        self.estado = FIN
        self.cartas_jugador = 0   # cartas del jugador que ya están en la mesa
        self.cartas_crupier = 0   # cartas del crupier que ya están en la mesa
        self.carta_oculta = True  # la segunda carta del crupier va boca abajo
        self.mensaje = ""
        self.color_mensaje = BLANCO
        self.marcador = {"ganadas": 0, "perdidas": 0, "empates": 0}

        self.crear_widgets()
        self.asignar_teclas()
        self.nueva_partida()

    # ------------------------------------------------------------------
    # Construcción de la ventana
    # ------------------------------------------------------------------

    def crear_widgets(self):
        """Crea el lienzo de la mesa y la barra de botones."""
        self.lienzo = tk.Canvas(
            self.raiz,
            width=round(ANCHO_MESA * self.escala),
            height=round(ALTO_MESA * self.escala),
            bg=VERDE_MESA,
            highlightthickness=0
        )
        self.lienzo.pack()

        barra = tk.Frame(self.raiz, bg=VERDE_OSCURO, pady=12)
        barra.pack(fill="x")

        self.boton_pedir = self.crear_boton(barra, "Pedir carta", self.pedir_carta)
        self.boton_plantarse = self.crear_boton(barra, "Plantarse", self.plantarse)
        self.boton_nueva = self.crear_boton(barra, "Nueva partida", self.nueva_partida)

        for boton in (self.boton_pedir, self.boton_plantarse, self.boton_nueva):
            boton.pack(side="left", expand=True)

    def crear_boton(self, padre, texto, accion):
        return tk.Button(
            padre,
            text=texto,
            command=accion,
            font=(FUENTE, 12, "bold"),
            width=16,
            pady=6,
            bg=DORADO,
            fg=NEGRO,
            activebackground=DORADO_CLARO,
            activeforeground=NEGRO,
            disabledforeground=GRIS_CLARO,
            relief="flat",
            cursor="hand2"
        )

    def asignar_teclas(self):
        """Atajos de teclado: P pide carta, S se planta, N reparte otra vez."""
        for tecla in ("p", "P"):
            self.raiz.bind(f"<KeyPress-{tecla}>", lambda evento: self.pedir_carta())

        for tecla in ("s", "S"):
            self.raiz.bind(f"<KeyPress-{tecla}>", lambda evento: self.plantarse())

        for tecla in ("n", "N"):
            self.raiz.bind(f"<KeyPress-{tecla}>", lambda evento: self.nueva_partida())

        self.raiz.bind("<Return>", lambda evento: self.nueva_partida())
        self.raiz.bind("<Escape>", lambda evento: self.salir())
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir)

    # ------------------------------------------------------------------
    # Flujo de la partida
    # ------------------------------------------------------------------

    def nueva_partida(self):
        """Empieza una partida nueva y reparte las cartas una a una."""
        if self.estado != FIN:
            return

        self.juego = JuegoBlackjack()
        self.cartas_jugador = 0
        self.cartas_crupier = 0
        self.carta_oculta = True
        self.estado = REPARTIENDO

        self.poner_mensaje("Repartiendo cartas...")
        self.actualizar_botones()
        self.dibujar_mesa()

        self.raiz.after(PAUSA_REPARTO, self.repartir_carta_inicial, 0)

    def repartir_carta_inicial(self, paso):
        """Enseña las cuatro primeras cartas: jugador, crupier, jugador, crupier."""
        if paso == 4:
            self.despues_del_reparto()
            return

        if paso % 2 == 0:
            self.cartas_jugador += 1
        else:
            self.cartas_crupier += 1

        self.dibujar_mesa()
        self.raiz.after(PAUSA_REPARTO, self.repartir_carta_inicial, paso + 1)

    def despues_del_reparto(self):
        """Si alguien tiene Blackjack la partida acaba; si no, juega el jugador."""
        if self.juego.terminado:
            self.terminar_partida()
            return

        self.estado = TURNO_JUGADOR
        self.poner_mensaje("Tu turno: ¿pides carta o te plantas?")
        self.actualizar_botones()
        self.dibujar_mesa()

    def pedir_carta(self):
        if self.estado != TURNO_JUGADOR:
            return

        self.juego.pedir_carta()
        self.cartas_jugador = len(self.juego.jugador)
        puntos = self.juego.obtener_puntuacion_jugador()

        if self.juego.terminado:
            self.empezar_turno_crupier(f"Tienes {puntos}: te has pasado de 21.")

        elif puntos == 21:
            # Con 21 no tiene sentido pedir más: se planta solo
            self.juego.plantarse()
            self.empezar_turno_crupier("¡Tienes 21! Ahora juega el crupier...")

        else:
            self.dibujar_mesa()

    def plantarse(self):
        if self.estado != TURNO_JUGADOR:
            return

        puntos = self.juego.obtener_puntuacion_jugador()

        # juego.py hace jugar al crupier y decide el ganador de una vez;
        # la interfaz enseña después sus cartas poco a poco
        self.juego.plantarse()
        self.empezar_turno_crupier(f"Te plantas con {puntos}. Juega el crupier...")

    def empezar_turno_crupier(self, mensaje):
        self.estado = TURNO_CRUPIER
        self.poner_mensaje(mensaje)
        self.actualizar_botones()
        self.dibujar_mesa()

        self.raiz.after(PAUSA_CRUPIER, self.descubrir_carta_oculta)

    def descubrir_carta_oculta(self):
        self.carta_oculta = False
        self.dibujar_mesa()

        self.raiz.after(PAUSA_CRUPIER, self.mostrar_carta_crupier)

    def mostrar_carta_crupier(self):
        """Enseña las cartas que ha pedido el crupier, una cada vez."""
        if self.cartas_crupier < len(self.juego.crupier):
            self.cartas_crupier += 1
            self.dibujar_mesa()
            self.raiz.after(PAUSA_CRUPIER, self.mostrar_carta_crupier)
        else:
            self.terminar_partida()

    def terminar_partida(self):
        """Enseña todas las cartas y el resultado, y suma la partida al marcador."""
        self.estado = FIN
        self.carta_oculta = False
        self.cartas_jugador = len(self.juego.jugador)
        self.cartas_crupier = len(self.juego.crupier)

        tipo = clasificar_resultado(self.juego.resultado)
        self.marcador[tipo] += 1

        colores = {"ganadas": DORADO, "perdidas": ROJO_CLARO, "empates": BLANCO}
        self.poner_mensaje(self.juego.resultado, colores[tipo])
        self.actualizar_botones()
        self.dibujar_mesa()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Quieres salir del Blackjack?", parent=self.raiz):
            self.raiz.destroy()

    # ------------------------------------------------------------------
    # Estado de los botones y del mensaje
    # ------------------------------------------------------------------

    def poner_mensaje(self, texto, color=BLANCO):
        self.mensaje = texto
        self.color_mensaje = color

    def actualizar_botones(self):
        """Solo se puede usar lo que tiene sentido en cada momento."""
        turno_jugador = self.estado == TURNO_JUGADOR

        self.activar_boton(self.boton_pedir, turno_jugador)
        self.activar_boton(self.boton_plantarse, turno_jugador)
        self.activar_boton(self.boton_nueva, self.estado == FIN)

    def activar_boton(self, boton, activo):
        if activo:
            boton.config(state="normal", bg=DORADO, cursor="hand2")
        else:
            boton.config(state="disabled", bg=VERDE_APAGADO, cursor="arrow")

    # ------------------------------------------------------------------
    # Dibujo de la mesa
    # ------------------------------------------------------------------

    def dibujar_mesa(self):
        """Borra el lienzo y vuelve a pintar todo según el estado actual."""
        lienzo = self.lienzo
        lienzo.delete("all")

        centro = ANCHO_MESA / 2

        rectangulo_redondeado(
            lienzo, 10, 10, ANCHO_MESA - 10, ALTO_MESA - 10, 30,
            fill="", outline=DORADO, width=3
        )

        lienzo.create_text(
            centro, 46, text="BLACKJACK",
            fill=DORADO, font=(FUENTE, 26, "bold")
        )
        lienzo.create_text(
            centro, 76, text="El crupier pide carta hasta tener 17",
            fill=GRIS_CLARO, font=(FUENTE, 10)
        )

        self.dibujar_marcador()

        # Crupier
        cartas = self.juego.crupier[:self.cartas_crupier]
        ocultar = self.carta_oculta and len(cartas) >= 2
        lienzo.create_text(
            centro, Y_CARTAS_CRUPIER - 18,
            text=f"CRUPIER   {self.texto_puntos_crupier(cartas, ocultar)}",
            fill=BLANCO, font=(FUENTE, 13, "bold")
        )
        self.dibujar_mano(cartas, Y_CARTAS_CRUPIER, ocultar)

        self.dibujar_mensaje()

        # Jugador
        cartas = self.juego.jugador[:self.cartas_jugador]
        self.dibujar_mano(cartas, Y_CARTAS_JUGADOR, False)
        lienzo.create_text(
            centro, Y_CARTAS_JUGADOR + ALTO_CARTA + 22,
            text=f"JUGADOR   {self.texto_puntos_jugador(cartas)}",
            fill=BLANCO, font=(FUENTE, 13, "bold")
        )

        lienzo.create_text(
            centro, ALTO_MESA - 32,
            text="Teclado:  P pedir carta   ·   S plantarse   ·   N nueva partida   ·   Esc salir",
            fill=GRIS_CLARO, font=(FUENTE, 10)
        )

        # Todo se dibuja a tamaño 100 % y se amplía si la pantalla tiene zoom
        if self.escala != 1:
            lienzo.scale("all", 0, 0, self.escala, self.escala)

    def dibujar_marcador(self):
        partidas = sum(self.marcador.values())

        if self.estado != FIN:
            partidas += 1

        self.lienzo.create_text(
            36, 32, anchor="nw",
            text=(
                f"Ganadas: {self.marcador['ganadas']}\n"
                f"Perdidas: {self.marcador['perdidas']}\n"
                f"Empates: {self.marcador['empates']}"
            ),
            fill=GRIS_CLARO, font=(FUENTE, 11)
        )
        self.lienzo.create_text(
            ANCHO_MESA - 36, 32, anchor="ne",
            text=f"Partida {partidas}",
            fill=GRIS_CLARO, font=(FUENTE, 11)
        )

    def dibujar_mensaje(self):
        centro = ANCHO_MESA / 2

        rectangulo_redondeado(
            self.lienzo, centro - 300, Y_MENSAJE - 28, centro + 300, Y_MENSAJE + 28, 14,
            fill=VERDE_OSCURO, outline=DORADO
        )

        if self.estado == FIN:
            self.lienzo.create_text(
                centro, Y_MENSAJE - 9, text=self.mensaje,
                fill=self.color_mensaje, font=(FUENTE, 15, "bold")
            )
            self.lienzo.create_text(
                centro, Y_MENSAJE + 15,
                text="Pulsa «Nueva partida» o la tecla N para jugar otra",
                fill=GRIS_CLARO, font=(FUENTE, 10)
            )
        else:
            self.lienzo.create_text(
                centro, Y_MENSAJE, text=self.mensaje,
                fill=self.color_mensaje, font=(FUENTE, 15, "bold")
            )

    def texto_puntos_crupier(self, cartas, ocultar):
        if not cartas:
            return ""

        if ocultar:
            # Solo se cuenta la carta que está boca arriba
            return f"{self.juego.calcular_puntuacion(cartas[:1])} + ?"

        return self.texto_puntos(cartas)

    def texto_puntos_jugador(self, cartas):
        if not cartas:
            return ""

        return self.texto_puntos(cartas)

    def texto_puntos(self, cartas):
        puntos = self.juego.calcular_puntuacion(cartas)

        if self.juego.es_blackjack(cartas):
            return f"{puntos}  ·  Blackjack"

        if puntos > 21:
            return f"{puntos}  ·  Se pasa"

        return str(puntos)

    def dibujar_mano(self, cartas, y, ocultar_segunda):
        """Coloca las cartas centradas; si son muchas, se solapan un poco."""
        if not cartas:
            return

        paso = ANCHO_CARTA + HUECO_CARTAS
        ancho_maximo = ANCHO_MESA - 160

        if len(cartas) > 1 and (len(cartas) - 1) * paso + ANCHO_CARTA > ancho_maximo:
            paso = (ancho_maximo - ANCHO_CARTA) / (len(cartas) - 1)

        ancho_total = (len(cartas) - 1) * paso + ANCHO_CARTA
        x = (ANCHO_MESA - ancho_total) / 2

        for posicion, carta in enumerate(cartas):
            if ocultar_segunda and posicion == 1:
                self.dibujar_reverso(x, y)
            else:
                self.dibujar_carta(x, y, carta)

            x += paso

    def dibujar_carta(self, x, y, carta):
        lienzo = self.lienzo
        color = ROJO if carta["palo"] in PALOS_ROJOS else NEGRO
        simbolo = SIMBOLOS[carta["palo"]]
        valor = "A" if carta["valor"] == "As" else carta["valor"]

        rectangulo_redondeado(
            lienzo, x + 4, y + 5, x + ANCHO_CARTA + 4, y + ALTO_CARTA + 5, 10,
            fill=SOMBRA, outline=""
        )
        rectangulo_redondeado(
            lienzo, x, y, x + ANCHO_CARTA, y + ALTO_CARTA, 10,
            fill=CARTA, outline=BORDE_CARTA
        )

        lienzo.create_text(
            x + 9, y + 7, anchor="nw", text=valor,
            fill=color, font=(FUENTE, 15, "bold")
        )
        lienzo.create_text(
            x + 10, y + 31, anchor="nw", text=simbolo,
            fill=color, font=(FUENTE, 13)
        )
        lienzo.create_text(
            x + ANCHO_CARTA / 2, y + ALTO_CARTA / 2 + 6, text=simbolo,
            fill=color, font=(FUENTE, 34)
        )
        lienzo.create_text(
            x + ANCHO_CARTA - 9, y + ALTO_CARTA - 7, anchor="se", text=valor,
            fill=color, font=(FUENTE, 15, "bold")
        )

    def dibujar_reverso(self, x, y):
        lienzo = self.lienzo

        rectangulo_redondeado(
            lienzo, x + 4, y + 5, x + ANCHO_CARTA + 4, y + ALTO_CARTA + 5, 10,
            fill=SOMBRA, outline=""
        )
        rectangulo_redondeado(
            lienzo, x, y, x + ANCHO_CARTA, y + ALTO_CARTA, 10,
            fill=AZUL_REVERSO, outline=BORDE_CARTA
        )
        rectangulo_redondeado(
            lienzo, x + 7, y + 7, x + ANCHO_CARTA - 7, y + ALTO_CARTA - 7, 6,
            fill="", outline=BLANCO, width=2
        )

        # Rombos decorativos
        for fila in range(5):
            for columna in range(3):
                cx = x + 23 + columna * 22
                cy = y + 21 + fila * 22
                lienzo.create_polygon(
                    cx, cy - 8, cx + 8, cy, cx, cy + 8, cx - 8, cy,
                    fill=AZUL_ROMBOS, outline=""
                )


def activar_alta_resolucion():
    """En Windows, evita que la ventana se vea borrosa si la pantalla tiene zoom."""
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass


def centrar_ventana(raiz):
    raiz.update_idletasks()
    x = (raiz.winfo_screenwidth() - raiz.winfo_width()) // 2
    y = (raiz.winfo_screenheight() - raiz.winfo_height()) // 3
    raiz.geometry(f"+{max(x, 0)}+{max(y, 0)}")


def iniciar_interfaz():
    """Abre la ventana del juego."""
    activar_alta_resolucion()

    raiz = tk.Tk()
    InterfazBlackjack(raiz)
    centrar_ventana(raiz)
    raiz.mainloop()
