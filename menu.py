import pygame
import sys
from juego import combate

# Inicializar Pygame
pygame.init()
pygame.mixer.init()  # ← INICIALIZA EL MÓDULO DE MÚSICA
ancho, alto = 1600, 900
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Heroes of the Black Storm")


# Reproducir música de fondo del menú
pygame.mixer.music.load("Audio/Musica/DS3 OST SYNTH.mp3")  # ← Ruta a tu canción
pygame.mixer.music.set_volume(1)  # Volumen (entre 0.0 y 1.0)
pygame.mixer.music.play(-1)  # -1 significa que se repite en bucle

# Colores
NEGRO = (0, 0, 0)
AZUL_OSCURO = (10, 10, 30)
GRIS_CLARO = (200, 200, 200)

# Cargar recursos
fondo = pygame.image.load("IMG/Fondo_menu.png").convert()
fondo = pygame.transform.scale(fondo, (ancho, alto))

fuente_botones = pygame.font.Font("Pixellari.ttf", 44)

# Estados
mostrar_controles = False

# Botones (centrados y grandes)
boton_ancho, boton_alto = 500, 100
boton_jugar = pygame.Rect(ancho // 2 - boton_ancho // 2, alto // 2 - 80, boton_ancho, boton_alto)
boton_controles = pygame.Rect(ancho // 2 - boton_ancho // 2, alto // 2 + boton_alto/2, boton_ancho, boton_alto)
boton_accesibilidad = pygame.Rect(ancho // 2 - boton_ancho // 2, alto // 2 + boton_alto * 2 -10, boton_ancho, boton_alto)


# Valores iniciales (por defecto)
valores = {
    "dano_prota": 5,
    "dano_dragon": 8,
    "cooldown_prota": 600,
    "invuln_prota": 1000,
    "invuln_dragon": 800,
    "musica": "Heroes of waterfalls-(recomendada).mp3",  # ← Recomendado
}


def dibujar_boton(rect, texto):
    # Colores basados en el título
    contorno = (48, 5, 11)
    fondo = (50, 62, 61)
    texto_color = (0, 0, 0)

    # Dibujar contorno
    pygame.draw.rect(ventana, contorno, rect.inflate(6, 6), border_radius=10)
    # Dibujar fondo del botón
    pygame.draw.rect(ventana, fondo, rect, border_radius=10)

    # Texto
    texto_render = fuente_botones.render(texto, True, texto_color)
    ventana.blit(
        texto_render,
        (rect.centerx - texto_render.get_width() // 2,
         rect.centery - texto_render.get_height() // 2)
    )

def mostrar_ventana_controles(ventana, fuente):
    ventana.fill((0, 0, 0))  # Fondo negro

    # Título
    texto = fuente.render("CONTROLES", True, (255, 255, 255))
    ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2, 50))

    # Tamaños personalizados
    tamaño_icono_normal = (64, 64)
    tamaño_icono_ancho = (96, 64)
    tamaño_spacebar = (128, 64)
    
    # Cargar y escalar imágenes
    img_up = pygame.transform.scale(pygame.image.load("IMG/Controles/k_up.png").convert_alpha(), tamaño_icono_normal)
    img_down = pygame.transform.scale(pygame.image.load("IMG/Controles/k_down.png").convert_alpha(), tamaño_icono_normal)
    img_left_right = pygame.transform.scale(pygame.image.load("IMG/Controles/k_right - k_left.png").convert_alpha(), tamaño_icono_ancho)
    img_spacebar = pygame.transform.scale(pygame.image.load("IMG/Controles/spacebar.png").convert_alpha(), tamaño_spacebar)

    controles = [
        ("    Moverse izquierda/derecha", img_left_right),
        ("Saltar", img_up),
        ("Esquivar/Sprint", img_down),
        ("        Atacar", img_spacebar),
    ]

    y = 150
    for texto, imagen in controles:
        ventana.blit(imagen, (100, y))
        txt = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(txt, (180, y + imagen.get_height() // 4))
        y += max(imagen.get_height(), 64) + 20  # para que no se amontonen
    
    # Instrucción para volver
    txt_volver = fuente.render("Presiona ENTER para volver", True, (200, 200, 200))
    ventana.blit(txt_volver, (ventana.get_width() // 2 - txt_volver.get_width() // 2, ventana.get_height() - 50))

def mostrar_configuracion_accesibilidad(ventana):
    
    fuente = pygame.font.Font("Pixellari.ttf", 36)
    clock = pygame.time.Clock()

    valores = {
        "dano_prota": 6,
        "dano_dragon": 8,
        "cooldown_prota": 600,
        "invuln_prota": 1000,
        "invuln_dragon": 800,
        "musica": "Heroes of waterfalls-(recomendada).mp3",  # ← Recomendado
    }

    musicas_disponibles = [
        "Heroes of waterfalls-(recomendada).mp3",  # Recomendado
        "Shadowlord (ver.1.22).mp3",
        "Midir OST SYNTH.mp3",
        "Dark Tower of Abyss.mp3",
        "Its Going Down Now.mp3",
        "Rage Against The Machine - Guerrilla Radio.mp3",
        "Dragor.mp3",
        "Emerald sword.mp3"
    ]
    
    

    etiquetas = list(valores.keys())
    indice = 0

    while True:
        clave_actual = etiquetas[indice]
        incremento = 100 if "cooldown" in clave_actual or "invuln" in clave_actual else 1

        for evento in pygame.event.get():
            linea = f"{clave.upper()}: {valores[clave]}" if clave != "musica" else f"MUSICA: {valores['musica']} (Recomendada)" if valores['musica'] == "Heroes of waterfalls-1.mp3" else f"MUSICA: {valores['musica']}"
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    # Guardar valores en archivo de configuración temporal
                    with open("accesibilidad_config.txt", "w") as f:
                        for k, v in valores.items():
                            f.write(f"{k}:{v}\n")
                    return valores
                elif evento.key == pygame.K_DOWN:
                    indice = (indice + 1) % len(etiquetas)
                elif evento.key == pygame.K_UP:
                    indice = (indice - 1) % len(etiquetas)
                elif evento.key == pygame.K_LEFT:
                    if clave_actual == "musica":
                        idx = musicas_disponibles.index(valores["musica"])
                        valores["musica"] = musicas_disponibles[(idx - 1) % len(musicas_disponibles)]
                    else:
                        valores[clave_actual] = max(0, valores[clave_actual] - incremento)
                elif evento.key == pygame.K_RIGHT:
                    if clave_actual == "musica":
                        idx = musicas_disponibles.index(valores["musica"])
                        valores["musica"] = musicas_disponibles[(idx + 1) % len(musicas_disponibles)]
                    else:
                        valores[clave_actual] += incremento
                

        ventana.fill((0, 0, 0))
        texto = fuente.render("AJUSTES DE ACCESIBILIDAD", True, (255, 255, 255))
        ventana.blit(texto, (ventana.get_width()//2 - texto.get_width()//2, 30))

        info_prota = fuente.render("Protagonista HP: 100", True, (255, 100, 100))
        info_dragon = fuente.render("Dragón HP: 300", True, (100, 200, 255))
        ventana.blit(info_prota, (100, 80))
        ventana.blit(info_dragon, (100, 120))
        

        for i, clave in enumerate(etiquetas):
            color = (0, 255, 0) if i == indice else (255, 255, 255)
            linea = f"{clave.upper()}: {valores[clave]}"
            texto = fuente.render(linea, True, color)
            ventana.blit(texto, (100, 220 + i * 50))

        instruccion = fuente.render("ENTER para aplicar y volver", True, (180, 180, 180))
        ventana.blit(instruccion, (ventana.get_width()//2 - instruccion.get_width()//2, ventana.get_height() - 60))
        
        pygame.display.flip()
        clock.tick(30)


# Bucle principal del menú
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        elif evento.type == pygame.KEYDOWN and mostrar_controles:
            if evento.key == pygame.K_RETURN:
                mostrar_controles = False
    
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if mostrar_controles:
                continue  # Ignorar clics mientras se muestran los controles
    
            if boton_jugar.collidepoint(evento.pos):
                print("Iniciando juego...")
                pygame.mixer.quit()
                pygame.quit()
                combate(valores)
                sys.exit()
    
            elif boton_controles.collidepoint(evento.pos):
                mostrar_controles = True
    
            elif boton_accesibilidad.collidepoint(evento.pos):
                valores = mostrar_configuracion_accesibilidad(ventana)




    if mostrar_controles:
        mostrar_ventana_controles(ventana, fuente_botones)
    else:
        ventana.blit(fondo, (0, 0))
        dibujar_boton(boton_jugar, "JUGAR")
        dibujar_boton(boton_controles, "CONTROLES")
        dibujar_boton(boton_accesibilidad, "ACCESIBILIDAD")


    pygame.display.flip()

