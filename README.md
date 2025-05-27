# Heroes of the Black Storm (asi se llama el juego)

*Heroes of the Black Storm* es un videojuego 2D desarrollado como parte de mis estudios universitarios, pero extendido más allá del requerimiento inicial como proyecto personal. utilizando Python y Pygame.

## Sobre el juego

Diseñado desde cero, el jugador controla a un protagonista con habilidades de movimiento, salto, sprint y ataque, enfrentándose a un dragón que evoluciona en mitad del combate. El juego incluye un menú interactivo, configuración de accesibilidad y música de fondo integrada.

## Lo que implementé

- Sistema de combate en tiempo real con IA para el jefe
- Animaciones por sprites (idle, correr, ataque)
- Mecánicas como salto, sprint, daño, colisiones, y fases de batalla
- Menú principal con controles y ajustes de accesibilidad
- Reproducción de música y efectos de sonido
- HUD dinámico con barra de vida

## Tecnologías utilizadas

- Python 3
- Pygame
- Recursos en formato `.png`, `.mp3` y `.wav`

## Estructura del proyecto

- `menu.py` → Menú principal con controles y accesibilidad
- `juego.py` → Lógica central del combate
- `bossdragon.py` → Comportamiento del dragón jefe
- `protagonista.py` → Movimiento y habilidades del personaje
- Carpeta `IMG/` → Sprites, animaciones y fondos
- Carpeta `Audio/` → Música y efectos
- Fuente `Pixellari.ttf` para los textos

## ▶️ Cómo ejecutarlo

1. Asegúrate de tener Python instalado.
2. Instala pygame si no lo tienes:
   ```bash
   pip install pygame
3. Ejecutalo en un compilador de codigo como vsc
