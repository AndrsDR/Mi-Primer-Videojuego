def combate(config):
    
    import pygame
    import random
    from protagonista import Protagonista
    from bossdragon import Dragon
    
    # Inicialización
    pygame.init()
    pygame.mixer.init()

    
    ANCHO, ALTO = 1600, 900
    ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)  # Permite redimensionar
    pygame.display.set_caption("Ashen Blood")

    fondo_combate = pygame.image.load("IMG/Fondo_combate.png").convert()
    fondo_combate = pygame.transform.scale(fondo_combate, (ANCHO, ALTO))

    piso = pygame.image.load("IMG/Piso.png").convert_alpha()
    piso = pygame.transform.scale(piso, (ANCHO, 140))  # Ajusta 80 si tu suelo es más alto o más bajo

    
    def posiciones_iniciales(ancho_ventana):
        prota_x = 100  # Margen izquierdo
        dragon_x = ancho_ventana - 300  # Margen derecho (ajusta 300 según tamaño del dragón)
        return prota_x, dragon_x
    
    # Colores
    BLANCO = (255, 255, 255)
    ROJO = (255, 0, 0)
    GRIS = (100, 100, 100)
    
    prota_x, dragon_x = posiciones_iniciales(ANCHO)
    protagonista = Protagonista(prota_x, 300, 140, 120)
    protagonista.dano = config["dano_prota"]
    protagonista.cooldown_ataque = config["cooldown_prota"]
    protagonista.invulnerabilidad_duracion = config["invuln_prota"]
    
    dragon = Dragon(ANCHO - 200, ALTO - 250, ANCHO)  # Borde derecho
    dragon.dano_ataque = config["dano_dragon"]
    dragon.duracion_invulnerabilidad = config["invuln_dragon"]
    
    
    
    
    # Configuración del piso
    piso_x, piso_ancho, piso_alto = 0, ANCHO, 100
    piso_y = ALTO - piso_alto
    
    # Bucle principal
    ejecutando = True
    reloj = pygame.time.Clock()
    FPS = 60
    
    
    pygame.mixer.music.load("Audio/Musica/" + config["musica"])
    pygame.mixer.music.set_volume(1)  # Puedes ajustar el volumen entre 0.0 y 1.0
    pygame.mixer.music.play(-1)  # -1 hace que la canción se repita infinitamente
    
    
    while ejecutando:
    
        ventana.blit(fondo_combate, (0, 0))

        # Manejo de eventos
        teclas = pygame.key.get_pressed()
    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            # Detección de ataques (dentro del bucle de eventos)
            if (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1) or (teclas[pygame.K_SPACE]):
                protagonista.atacar()
        
        # Entradas de teclado continuas
        if teclas[pygame.K_ESCAPE]:
            ejecutando = False
        
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            protagonista.mover_izquierda(FPS)
        else:
            protagonista.cont_izq = 0
        
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            protagonista.mover_derecha(FPS)
        else:
            protagonista.cont_der = 0
        
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            protagonista.saltar(piso_y)
    
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            protagonista.activar_sprint()
    
        if dragon.Fase_combate == 2:
            dragon.rayo_fijado_cont += 1
            if dragon.rayo_fijado_cont == 1:
                dragon.activar_rayo_fijo(protagonista)
    
    
    
        tiempo_actual = pygame.time.get_ticks()

        # Daño gradual al dragón en Fase 2
        if dragon.Fase_combate == 2 and dragon.vida_actual > 0:
            if tiempo_actual - dragon.tiempo_ultimo_dano_gradual >= dragon.intervalo_dano_gradual:
                dragon.vida_actual -= dragon.dano_por_segundo
                dragon.tiempo_ultimo_dano_gradual = tiempo_actual

    
    
    
        if abs(dragon.rect.centerx - protagonista.rect.centerx) > ANCHO/2 and not dragon.atacando:
            if dragon.Fase_combate == 1:
                dragon.activar_rayo_escupido()
            elif dragon.Fase_combate == 2:
                if random.randint(1, 2) == 1:
                    dragon.activar_rayo_escupido()
                else:
                    dragon.iniciar_ataque_embestida(piso_y)
        elif not dragon.atacando:
            if dragon.Fase_combate == 2:
                dragon.iniciar_combo_garras()
                if random.randint(1, 2) == 1:
                    dragon.iniciar_combo_garras()
                else:
                    dragon.iniciar_ataque_embestida(piso_y)
            else:
                dragon.iniciar_combo_garras()
                
    
    
        # Dentro del while ejecutando:
        if dragon.rect_ataque and dragon.rect_ataque.colliderect(protagonista.rect):
            if not protagonista.invulnerable:  # Asegúrate de tener este atributo
                protagonista.recibir_dano(dragon.dano_ataque)
                protagonista.invulnerable = True
                protagonista.tiempo_invulnerable = pygame.time.get_ticks()
            
        # Añade también para quitar la invulnerabilidad después de un tiempo
        if protagonista.invulnerable and pygame.time.get_ticks() - protagonista.tiempo_invulnerable > 1000:
            protagonista.invulnerable = False
        
        # Verificar colisión ataque prota -> dragón (solo si no está atacando)
        if (protagonista.rect_ataque and 
            protagonista.rect_ataque.colliderect(dragon.rect)):
            dragon.recibir_dano(protagonista.dano)  # Ajusta el daño según necesidad
    
        
        protagonista.dibujar(ventana)
        protagonista.sprint()
        protagonista.actualizar_sprint_cooldown()
    
        # Actualizar física
        protagonista.actualizar_fisica(piso_y, ANCHO)
        dragon.actualizar(protagonista, piso_y)
    
        dragon.dibujar(ventana,protagonista)  # La barra de vida ya está incluida aquí
        vida_prota_width = int(200 * (protagonista.vida / 100))  # Asume que vida máxima es 100
        pygame.draw.rect(ventana, (255, 0, 0), (20, 20, 200, 20))
        pygame.draw.rect(ventana, (0, 255, 0), (20, 20, vida_prota_width, 20))
        ventana.blit(piso, (piso_x, piso_y))


    
        
        if dragon.vida_actual <= dragon.vida_max / 3 and dragon.Fase_combate == 1:
            dragon.Fase_combate = 2
            protagonista.dano /= 2
            dragon.dano_ataque *= 2
    
            
        if dragon.vida_actual <= dragon.vida_max / 3:
            dragon.Fase_combate = 2

            # GAME OVER o GANASTE
        if protagonista.vida <= 0 or dragon.vida_actual <= 0:
            ventana.fill((0, 0, 0))  # Borra todo
        
            fuente = pygame.font.SysFont("arial", 100, bold=True)
            if protagonista.vida <= 0:
                texto = fuente.render("GAME OVER", True, (255, 0, 0))
                texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
                ventana.blit(texto, texto_rect)
            else:
                texto = fuente.render("GANASTE", True, (0, 255, 0))
                texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
                ventana.blit(texto, texto_rect)
            pygame.display.flip()
            ejecutando = False
            if protagonista.vida <= 0:
                pygame.time.delay(3000)
            else:
                pygame.time.delay(10000)
            continue
        
        pygame.display.flip()
        
    
        reloj.tick(FPS)
    
    pygame.mixer.music.stop()
    pygame.quit()