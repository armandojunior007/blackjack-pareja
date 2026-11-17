
# Blackjack - Proyecto en pareja

## Descripción
Juego de Blackjack desarrollado con Python como práctica de Git y GitHub.

## Integrantes
- Armando Shuguli
- Daniel Sanz

## Requisitos
- Python 3 instalado (incluye tkinter, que se usa para la ventana).
- En Linux puede hacer falta instalarlo aparte: `sudo apt install python3-tk`.

## Ejecución
Desde la terminal, en la carpeta del proyecto:

```
python main.py
```

Abre el juego en una ventana. Para jugar en la terminal, como en la primera versión:

```
python main.py --consola
```

Si tkinter no está instalado, el juego se abre directamente por consola.

## Controles
| Acción | Botón | Tecla |
| --- | --- | --- |
| Pedir carta | Pedir carta | P |
| Plantarse | Plantarse | S |
| Jugar otra partida | Nueva partida | N o Intro |
| Salir | Cerrar la ventana | Esc |

Cada botón solo está activo cuando se puede usar.

## Flujo de una partida
1. Se reparten las cartas una a una: jugador, crupier, jugador, crupier. La segunda carta del crupier queda boca abajo.
2. Si alguien tiene Blackjack con las dos primeras cartas, la partida acaba.
3. Turno del jugador: pide cartas o se planta. Si se pasa de 21 pierde, y si llega a 21 se planta solo.
4. Turno del crupier: descubre su carta oculta y pide cartas hasta tener 17.
5. Se muestra el resultado y se suma al marcador (ganadas, perdidas y empates) de la sesión.

## Reglas
- El objetivo es acercarse a 21 puntos sin pasarse.
- El jugador puede pedir cartas o plantarse.
- El As vale 11 o 1 según convenga.
- El crupier pide cartas hasta alcanzar 17 puntos.
- Gana quien tenga la puntuación más alta sin superar 21.

## Organización
- main.py: arranca el juego en la ventana o en la consola.
- cartas.py: crea y reparte las cartas.
- juego.py: contiene las reglas y la lógica.
- interfaz.py: interfaz gráfica (tkinter): mesa, botones, teclado y flujo de la partida.
- consola.py: versión del juego por consola.
