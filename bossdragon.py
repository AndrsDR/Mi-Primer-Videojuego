import pygame
import math
import random

class Dragon:
    def __init__(self, x, y, ancho_ventana):
        """
        Constructor de la clase Dragon.
        Aquí se inicializan todas las variables necesarias para manejar el estado, ataques y animaciones del dragón.
        """

        # VIDA Y DAÑO
        self.vida_max = 300                          # Vida máxima del dragón
        self.vida_actual = self.vida_max             # Vida actual
        self.dano_ataque = 7                     # Daño que inflige con cada ataque

        # FÍSICA BÁSICA
        self.velocidad_normal = 0                    # No se usa por ahora, pero puede usarse para caminar
        self.volando = False                         # Indica si está en el aire
        self.en_suelo = True                         # Indica si está tocando el piso
        self.velocidad_y = 0                         # Velocidad en eje Y (para simular gravedad)
        self.gravedad = 0.8                          # Aceleración gravitacional
        self.ancho_ventana = ancho_ventana           # Límite derecho para ataques como embestida o vuelo
        self.altura_suelo = y + 150               # Y del piso donde aterriza (se puede modificar según sprite)

        # COLLISION RECT (tamaño del dragón)
        self.ancho_dragon = 400
        self.altura_dragon = 300
        self.rect = pygame.Rect(x, y, self.ancho_dragon, self.altura_dragon)      # Posición y tamaño del dragón en pantalla
        self.color_base = (255, 200, 0)              # Color del dragón (sólo si usas un rectángulo de depuración)

        # ATAQUE GENERAL (usa esto embestida y combo para bloquear acciones)
        self.atacando = False                        # Indica si el dragón está en medio de un ataque
        self.rect_ataque = None                      # Hitbox del ataque (rect rojo que daña)
        self.tiempo_inicio_ataque = 0                # Marca de tiempo para manejar fases y delays
        self.duracion_ataque = 2000                  # Duración genérica de ataque (no muy usado)

        # EMBESTIDA (fase 1 del jefe)
        self.direccion_ataque = -1                   # -1 si va hacia la izquierda, 1 si va hacia la derecha
        self.fase_ataque = 0                         # Fase de la animación de embestida
        self.embestida_alzamiento = 10               # Qué tanto se eleva al principio del ataque
        self.velocidad_embestida = 18                # Velocidad horizontal de la embestida
        self.atque_embestida = False

        # ORIENTACIÓN
        self.mirando_derecha = False                 # Dirección visual (usada para saber hacia dónde atacar)

        # ATAQUE DE RAYOS (fase 2 del jefe)
        self.rayos = []                              # Lista de rayos activos (cada uno es un dict con posición y ángulo)
        self.tiempo_ultimo_rayo = -99999             # Última vez que lanzó un rayo (para cooldown)
        self.duracion_rayos = 3500                   # Cuánto tiempo persiguen los rayos
        self.cooldown_rayos = 5000                   # Tiempo entre usos del ataque de rayos
        self.fase_ataque_rayos = -1                  # Fase del ataque de rayos (-1 = inactivo)
        self.altura_objetivo_vuelo = 50              # Altura que alcanza al volar antes de lanzar rayos
        self.direccion_vuelo = -1                    # Dirección del vuelo (-1 izquierda, 1 derecha)
        self.max_rayos = 0                           # Cuántos rayos se lanzarán (aleatorio entre 3 y 5)
        self.rayos_lanzados = 0                      # Cuántos rayos se han lanzado ya
        self.posicion_destino = x                    # Punto final del vuelo, usado para saber cuándo aterrizar

        # ATAQUE COMBO (fase 1, golpe - golpe - mordida)
        self.fase_combo = -1                         # Fase del combo (-1 = inactivo, 0-3 = pasos del ataque)
        self.tiempo_combo = 0                        # Marca de tiempo para manejar los tiempos entre golpes
        self.tiempo_hitbox_combo = 0                 # Tiempo de duración de la hitbox actual del combo
        self.combo_activo = False                    # Se usa para distinguir combo de embestida

        # Rayo Fijado
        self.rayo_fijado_activo = False
        self.fase_rayo = 0
        self.rayo_fijo_pos = (0,0)
        self.tiempo_fase_rayo = 0 
        self.rayo_fijado_cont = 0

        #Escupir Rayo
        self.escupir_rayo_tiempo_activar = 0
        self.escupir_rayo_tiempo = 0
        self.rayo_escupido_altura = self.rect.height / 4
        self.rayo_escupido_activo = False

        # ALIENTO DE RAYO (Fase 2)
        self.Fase_combate = 2              # Cambia a 1 si estás en fase 1
        self.rayo_aliento_activo = False   # Indica si el rayo está activo
        self.tiempo_aliento = 0            # Marca cuándo comenzó el aliento
        

        self.impacto_suelo_activo = False
        self.tiempo_impacto_suelo = 0
        self.rect_impacto_suelo = None



        self.Fase_combate = 1
        self.ataques_en_suelo = True

        self.tiempo_ultimo_dano_gradual = 0
        self.intervalo_dano_gradual = 100  # en milisegundos
        self.dano_por_segundo = .25         # ajusta esto según qué tan rápido quieres que muera
        


        # INVULNERABILIDAD
        self.invulnerable = False                    # Si está invulnerable (tras recibir daño)
        self.tiempo_invulnerable = 0 


        self.sprite_idle = pygame.image.load("IMG/Vorthzhar/Dragon_base.png").convert_alpha()
        self.sprite_idle = pygame.transform.scale(self.sprite_idle, (self.ancho_dragon, self.altura_dragon))
        self.sprite_idle_disponible = True

        self.sprite_cargando_rayo = pygame.image.load("IMG/Vorthzhar/Ataque_escupir_rayo/Dragon_cargando_rayo.png").convert_alpha()
        self.sprite_cargando_rayo = pygame.transform.scale(self.sprite_cargando_rayo, (self.ancho_dragon, self.altura_dragon))
        self.sprite_cargando_rayo_disponible = False

        self.sprite_escupiendo_rayo = pygame.image.load("IMG/Vorthzhar/Ataque_escupir_rayo/Dragon_escupiendo_rayo.png").convert_alpha()
        self.sprite_escupiendo_rayo_disponible = False
        
        # Animación alzamiento (ataque en vuelo)
        self.sprites_ascendiendo = [
            pygame.image.load("IMG/Vorthzhar/Ataque_en_vuelo/Ascendiendo/Dragon_alzandoce_frame1.png").convert_alpha(),
            pygame.image.load("IMG/Vorthzhar/Ataque_en_vuelo/Ascendiendo/Dragon_alzandoce_frame2.png").convert_alpha()
        ]
        self.frame_actual_ascenso = 0
        self.tiempo_ultimo_frame_ascenso = 0
        self.sprite_ascendiendo_disponible = False
        

        # Animación de vuelo horizontal
        self.sprites_volando_horizontal = [
            pygame.image.load("IMG/Vorthzhar/Ataque_en_vuelo/Linea_Recta/Dragon_volando_horizontal_frame1.png").convert_alpha(),
            pygame.image.load("IMG/Vorthzhar/Ataque_en_vuelo/Linea_Recta/Dragon_volando_horizontal_frame2.png").convert_alpha()
        ]
        self.frame_actual_vuelo_horizontal = 0
        self.tiempo_ultimo_frame_vuelo_horizontal = 0
        self.sprite_volando_horizontal_disponible = False

        self.sprite_descendiendo = pygame.image.load("IMG/Vorthzhar/Ataque_en_vuelo/Dragon_descendiendo.png").convert_alpha()
        self.sprite_descendiendo_disponible = False
        
        # Sprites del ataque combo
        self.sprites_combo_garra = [
            pygame.image.load("IMG/Vorthzhar/Combo/Dragon_garra1.png").convert_alpha(),
            pygame.image.load("IMG/Vorthzhar/Combo/Dragon_garra2.png").convert_alpha()
        ]
        self.sprite_combo_mordida = pygame.image.load("IMG/Vorthzhar/Combo/Dragon_mordizco.png").convert_alpha()
        
        self.sprite_combo_disponible = False
        self.sprite_combo_fase = None

        self.sprite_embestida_ascendiendo = pygame.image.load("IMG/Vorthzhar/Embestida/Dragon_ascendiendo.png").convert_alpha()
        self.sprite_embestida_ascendiendo_disponible = False

        self.sprite_embistiendo = pygame.image.load("IMG/Vorthzhar/Embestida/Dragon_embistiendo.png").convert_alpha()
        self.sprite_embistiendo_disponible = False

        self.sprite_rayo_escupido = pygame.image.load("IMG/Vorthzhar/Rayos/Aliento.png").convert_alpha()

        self.sprites_teledirigidos = [
            pygame.image.load("IMG/Vorthzhar/Rayos/Teledirijidos/frame1.png").convert_alpha(),
            pygame.image.load("IMG/Vorthzhar/Rayos/Teledirijidos/frame2.png").convert_alpha()
        ]
        self.frame_actual_teledirigido = 0
        self.ultimo_cambio_frame_teledirigido = pygame.time.get_ticks()
        self.lista_rayos_teledirigidos = []  # Lista de pygame.Rect de rayos activos

        self.sprite_rayo_fisico = pygame.image.load("IMG/Vorthzhar/Rayos/fisico.png").convert_alpha()
        

        self.sprites_rayo_fijado = [
            pygame.image.load("IMG/Vorthzhar/Rayos/Fijado/frame1.png").convert_alpha(),
            pygame.image.load("IMG/Vorthzhar/Rayos/Fijado/frame2.png").convert_alpha()
        ]
        self.frame_actual_fijado = 0
        self.tiempo_ultimo_frame_fijado = pygame.time.get_ticks()

        self.sprite_impacto_suelo = pygame.image.load("IMG/Vorthzhar/Rayos/Aterrizaje.png").convert_alpha()

        self.sonido_aliento = pygame.mixer.Sound("Audio\Efecto de sonido\Shin godzilla atomic breath sound effects for sticknodes.wav")

        





    def activar_rayo_escupido(self):

        if not self.atacando and self.fase_ataque_rayos == -1 and self.ataques_en_suelo:

            self.rayo_escupido_activo = True
            self.escupir_rayo_tiempo_activar += 1
            if self.escupir_rayo_tiempo_activar == 1:
                self.tiempo_rayo_escupido = pygame.time.get_ticks()

        

    def dibujar_rayo_escupido(self, ventana, protagonista):
        if not self.rayo_escupido_activo:
            return
    
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_rayo_escupido > 500:
            self.sprite_idle_disponible = False
            self.sprite_cargando_rayo_disponible = True

        if tiempo_actual - self.tiempo_rayo_escupido > 1000:
            self.sprite_cargando_rayo_disponible = False
            self.sprite_escupiendo_rayo_disponible = True

            if self.mirando_derecha:
                x = self.rect.right
            else:
                x = self.rect.right - self.ancho_ventana - self.ancho_dragon
    
            y =  self.rect.y + (self.rect.height / 2)
    
            rayo_escupido = pygame.Rect(x,y ,self.ancho_ventana, self.rayo_escupido_altura)
    
            sprite = pygame.transform.scale(self.sprite_rayo_escupido, (rayo_escupido.width, rayo_escupido.height*1.85))

            if self.mirando_derecha:
                ventana.blit(sprite, (rayo_escupido.x, rayo_escupido.y -40))
            else:
                sprite_volteado = pygame.transform.flip(sprite, True, False)
                ventana.blit(sprite_volteado, (rayo_escupido.x, rayo_escupido.y -40))


            if rayo_escupido.colliderect(protagonista.rect):
                protagonista.recibir_dano(self.dano_ataque)
    
        if tiempo_actual - self.tiempo_rayo_escupido > 1300:
                self.escupir_rayo_tiempo_activar = 0
                self.rayo_escupido_activo = False
                self.ataques_en_suelo = False
                self.sprite_escupiendo_rayo_disponible = False
                self.iniciar_ataque_rayos(protagonista)
        
    def activar_rayo_fijo(self,protagonista):
        self.rayo_fijado_activo = True
        self.tiempo_rayo_fijo = pygame.time.get_ticks()
        self.rayo_fijo_pos = protagonista.rect.center  
        self.rayo_fijado_primera_vez = True            


    def actualizar_rayo_fijo_ciclico(self, protagonista):
        if not self.rayo_fijado_activo:
            return

        # Alterna entre los 2 frames cada 300ms
        if pygame.time.get_ticks() - self.tiempo_ultimo_frame_fijado > 300:
            self.frame_actual_fijado = (self.frame_actual_fijado + 1) % len(self.sprites_rayo_fijado)
            self.tiempo_ultimo_frame_fijado = pygame.time.get_ticks()
        
        
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_fase_rayo

        if self.fase_rayo == 0 and tiempo_transcurrido > 0:
            # 2s después → aparece el cuadrado
            self.fase_rayo = 1
            self.tiempo_fase_rayo = tiempo_actual
    
        elif self.fase_rayo == 1 and tiempo_transcurrido > 2500:
            # 3s después → crece y hace daño
            self.fase_rayo = 2
            self.tiempo_fase_rayo = tiempo_actual
    
        elif self.fase_rayo == 2 and tiempo_transcurrido > 1000:
            # 1s después → desaparece
            self.fase_rayo = 3
            self.tiempo_fase_rayo = tiempo_actual
    
        elif self.fase_rayo == 3 and tiempo_transcurrido > 2000:
            # 2s después → reinicia
            self.rayo_fijado_cont = 0
            self.fase_rayo = 0
            self.tiempo_fase_rayo = tiempo_actual
            self.rayo_fijo_pos = protagonista.rect.center  # se guarda nueva posición
    
    def dibujar_rayo_fijo(self, ventana, protagonista):
        if self.fase_rayo not in [1, 2]:
            return
    
        tamaño = 50
        frame = self.sprites_rayo_fijado[0]  # frame 1 por defecto
    
        if self.fase_rayo == 2:
            tamaño *= 2  # explota = el doble de tamaño
            frame = self.sprites_rayo_fijado[1]  # usar frame 2 (explosión)
    
            if protagonista.rect.collidepoint(self.rayo_fijo_pos):
                protagonista.recibir_dano(self.dano_ataque)
    
        x, y = self.rayo_fijo_pos
        rect_rayo = pygame.Rect(x - tamaño // 2, y - tamaño // 2, tamaño, tamaño)
    
        sprite_escalado = pygame.transform.scale(frame, (int(rect_rayo.width * 1.2), int(rect_rayo.height * 1.2)))
        rect_dibujo = sprite_escalado.get_rect(center=rect_rayo.center)
    
        ventana.blit(sprite_escalado, rect_dibujo)
    


    def iniciar_combo_garras(self):
        """
        Inicia el ataque en combo: zarpazo - zarpazo - mordida.
        Se bloquea si ya está atacando o si está en el aire (volando con rayos).
        """

        if not self.atacando and self.fase_ataque_rayos == -1 and self.ataques_en_suelo:
            self.atacando = True              # Bloquea otros ataques mientras dura
            self.combo_activo = True          # Marca que es un combo (no embestida)
            self.fase_combo = -1              # -1 activa la preparación (delay)
            self.tiempo_combo = pygame.time.get_ticks()  # Marca de tiempo para contar el delay




    def iniciar_ataque_embestida(self, piso_y):
        """
        Inicia el ataque de embestida del dragón: se alza, embiste y aterriza.
        """
        if not self.atacando and self.fase_ataque_rayos == -1 and not self.rayo_escupido_activo:
            self.atacando = True
            self.volando = True
            self.atque_embestida = True
            self.tiempo_inicio_ataque = pygame.time.get_ticks()
            self.direccion_ataque = 1 if self.mirando_derecha else -1  # Dirección depende de hacia dónde mira
            self.fase_ataque = 0
            self.altura_suelo = piso_y  # Actualiza el suelo por si cambia por entorno dinámico

    def actualizar_hitbox_ataque(self):
        """
        Crea la hitbox del ataque frontal según hacia dónde mira el dragón.
        """
        if self.direccion_ataque == 1:
            self.rect_ataque = pygame.Rect(self.rect.right, self.rect.centery - 40, 60, 80)
        else:
            self.rect_ataque = pygame.Rect(self.rect.left - 60, self.rect.centery - 40, 60, 80)

    def actualizar_ataque_embestida(self, protagonista):
        """
        Controla las fases del ataque de embestida:
        0 → alzamiento
        1 → avance hasta tocar el suelo
        2 → barrido horizontal
        3 → subida final
        4 → caída y finalización
        """
        tiempo_actual = pygame.time.get_ticks()
    
        if self.fase_ataque == 0:
            self.sprite_idle_disponible = False
            self.sprite_embestida_ascendiendo_disponible = True
            self.rect.y -= self.embestida_alzamiento
            if tiempo_actual - self.tiempo_inicio_ataque > 300:
                self.fase_ataque = 1
                self.sprite_embestida_ascendiendo_disponible = False
    
        elif self.fase_ataque == 1:
            self.sprite_embistiendo_disponible = True
            if self.rect.y < self.altura_suelo - self.rect.height:
                self.rect.y += self.embestida_alzamiento
                self.rect.x += self.direccion_ataque * self.velocidad_embestida
                self.actualizar_hitbox_ataque()
            else:
                self.rect.y = self.altura_suelo - self.rect.height
                self.fase_ataque = 2
                self.tiempo_inicio_ataque = tiempo_actual
    
        elif self.fase_ataque == 2:
            self.rect.x += self.direccion_ataque * self.velocidad_embestida
            self.actualizar_hitbox_ataque()
    
            # Termina cuando toca el borde
            if (self.direccion_ataque == 1 and self.rect.right >= self.ancho_ventana) or \
                (self.direccion_ataque == -1 and self.rect.left <= 0):
                self.fase_ataque = 3
                self.tiempo_inicio_ataque = tiempo_actual
    
        elif self.fase_ataque == 3:
            self.sprite_embistiendo_disponible = False
            self.sprite_embestida_ascendiendo_disponible = True
            self.rect.y -= 8  # pequeña subida antes de caer
            self.rect_ataque = None
            if tiempo_actual - self.tiempo_inicio_ataque > 300:
                self.fase_ataque = 4
    
        elif self.fase_ataque == 4:
            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y
            if self.rect.y >= self.altura_suelo - self.rect.height:
                self.sprite_embestida_ascendiendo_disponible = False
                self.rect.y = self.altura_suelo - self.rect.height
                self.velocidad_y = 0
                self.atque_embestida = False
                self.finalizar_ataque()
                self.sprite_idle_disponible = True
                # Decide siguiente ataque por probabilidad
                prob = random.randint(1, 100)
                
                if prob <= 40:
                    self.iniciar_ataque_embestida(self.altura_suelo)
                elif prob <= 65:
                    self.iniciar_ataque_rayos(protagonista)  # ← Asegúrate de pasar al protagonista
                    self.sprite_idle_disponible = False
                elif prob <= 90:
                    self.iniciar_combo_garras()
                else:
                    self.activar_rayo_escupido()


    def finalizar_ataque(self):
        """
        Limpia las variables una vez que el ataque ha terminado.
        Se usa para cualquier tipo de ataque.
        """
        self.atacando = False
        self.volando = False
        self.rect_ataque = None
        self.combo_activo = False
        self.mirando_derecha = self.rect.centerx < self.ancho_ventana // 2  # Se actualiza orientación

    def iniciar_ataque_rayos(self, protagonista):
        """
        Inicia el ataque de rayos teledirigidos. El dragón se eleva, vuela hacia el otro lado
        mientras lanza rayos que persiguen al protagonista.
        """
        tiempo_actual = pygame.time.get_ticks()
        if not self.atacando and self.fase_ataque_rayos == -1:
            self.tiempo_ultimo_rayo = tiempo_actual - 700  # le damos un headstart al primer rayo
            self.rayos = []
            self.fase_ataque_rayos = 0                     # Comienza la fase de vuelo ascendente
            self.direccion_vuelo = 1 if self.mirando_derecha else -1
            self.rayos_lanzados = 0
            self.max_rayos = random.randint(3, 5)          # Número aleatorio de rayos
            self.posicion_destino = 0 if self.direccion_vuelo == -1 else self.ancho_ventana - self.rect.width
            self.atacando = False
            


    def actualizar_ataque_rayos_en_vuelo(self, protagonista):
        """
        Fase 0: se eleva
        Fase 1: avanza horizontalmente lanzando rayos
        Fase 2: desciende al suelo
        """
        tiempo_actual = pygame.time.get_ticks()
    
    
        if self.fase_ataque_rayos == 0:
            # Fase inicial: el dragón sube
            self.rect.y -= 5

            self.sprite_idle_disponible = False
            self.sprite_ascendiendo_disponible = True

            # Animación de ascenso (cambia cada 120 ms)
            if tiempo_actual - self.tiempo_ultimo_frame_ascenso > 650:
                self.frame_actual_ascenso = (self.frame_actual_ascenso + 1) % len(self.sprites_ascendiendo)
                self.tiempo_ultimo_frame_ascenso = tiempo_actual

            if self.rect.y <= self.altura_objetivo_vuelo:
                self.fase_ataque_rayos = 1
                self.tiempo_inicio_vuelo = tiempo_actual
    
        elif self.fase_ataque_rayos == 1:
            self.sprite_ascendiendo_disponible = False
            self.sprite_volando_horizontal_disponible = True

            # Animación de vuelo horizontal (cambia cada 100ms)
            if tiempo_actual - self.tiempo_ultimo_frame_vuelo_horizontal > 700:
                self.frame_actual_vuelo_horizontal = (self.frame_actual_vuelo_horizontal + 1) % len(self.sprites_volando_horizontal)
                self.tiempo_ultimo_frame_vuelo_horizontal = tiempo_actual

            # Fase de vuelo horizontal
            if (self.direccion_vuelo == -1 and self.rect.left > self.posicion_destino) or \
                (self.direccion_vuelo == 1 and self.rect.left < self.posicion_destino):
                self.rect.x += self.direccion_vuelo * 5
    
                if self.Fase_combate == 1:
                    # Fase 1: lanza rayos teledirigidos
                    if (tiempo_actual - self.tiempo_ultimo_rayo > 700 and self.rayos_lanzados < self.max_rayos):
                        if self.mirando_derecha:
                            boca_x = self.rect.right
                            angulo = 45  # hacia abajo derecha
                        else:
                            boca_x = self.rect.left
                            angulo = 135  # hacia abajo izquierda
                        boca_y = self.rect.top + self.rect.height // 2
                        self.rayos.append({
                            "pos": [boca_x, self.rect.centery],
                            "angle": angulo,
                            "inicio": tiempo_actual,
                            "tipo": "teledirigido"
                        })
                        self.tiempo_ultimo_rayo = tiempo_actual
                        self.rayos_lanzados += 1
    
                elif self.Fase_combate == 2:
                    # Fase 2: rayo largo diagonal desde la boca
                    if not self.rayo_aliento_activo:
                        self.rayo_aliento_activo = True
                        self.tiempo_aliento = tiempo_actual

            else:
                self.fase_ataque_rayos = 2

        elif self.fase_ataque_rayos == 2:
            self.rayo_aliento_activo = False
            self.sprite_volando_horizontal_disponible = False
            self.sprite_descendiendo_disponible = True
            # Fase final: descenso
            self.rect.y += 5
            
            if self.rect.bottom >= self.altura_suelo:
                self.rect.y = self.altura_suelo - self.rect.height
                self.fase_ataque_rayos = -1
                self.mirando_derecha = self.rect.centerx < self.ancho_ventana // 2
                self.rayo_aliento_activo = False
                self.ataques_en_suelo = True
                self.sprite_idle_disponible = True
                self.sprite_descendiendo_disponible = False
        
                # Activar impacto en el suelo
                self.impacto_suelo_activo = True
                self.tiempo_impacto_suelo = pygame.time.get_ticks()
                self.rect_impacto_suelo = pygame.Rect(
                    self.rect.centerx - (self.ancho_dragon/1.2),  # puedes ajustar el ancho
                    self.altura_suelo - self.altura_dragon * .25 ,   # a ras del suelo
                    self.ancho_dragon * 1.5, self.altura_dragon * .25                   # ancho y alto de la hitbox
                )

    
    def actualizar_rayos(self, protagonista):
        """
        Actualiza todos los rayos activos, los mueve hacia el protagonista
        y chequea si lo golpean.
        """
        tiempo_actual = pygame.time.get_ticks()

        for rayo in self.rayos:
            if tiempo_actual - rayo["inicio"] > self.duracion_rayos:
                continue  # ya expiró
    
            rayo_x, rayo_y = rayo["pos"]
            objetivo_x = protagonista.rect.centerx
            objetivo_y = protagonista.rect.centery
    
            dx = objetivo_x - rayo_x
            dy = objetivo_y - rayo_y
            distancia = math.hypot(dx, dy)
            if distancia == 0:
                continue
            dx /= distancia
            dy /= distancia
    
            velocidad = 4
            rayo["pos"][0] += dx * velocidad
            rayo["pos"][1] += dy * velocidad
    
            rayo["angle"] = math.degrees(math.atan2(-dy, dx))  # para que "apunte" al prota
    
            # Colisión con el jugador
            rayo_rect = pygame.Rect(rayo["pos"][0] - 20, rayo["pos"][1] - 20, 40, 40)
            if rayo_rect.colliderect(protagonista.rect):
                protagonista.recibir_dano(self.dano_ataque)
    
        # Remover rayos viejos
        self.rayos = [r for r in self.rayos if tiempo_actual - r["inicio"] <= self.duracion_rayos]
    
    def dibujar_ataque_rayos(self, ventana, protagonista):
        # Dibujar rayos teledirigidos normales

        for rayo in self.rayos:
            if rayo.get("tipo") == "teledirigido":
                x, y = rayo["pos"]
                tam = 40
                sprite = self.sprites_teledirigidos[self.frame_actual_teledirigido]
                sprite_escalado = pygame.transform.scale(sprite, (tam* 1.5, tam*1.5))
                sprite_rotado = pygame.transform.rotate(sprite_escalado, rayo["angle"])
                rect_rotado = sprite_rotado.get_rect(center=(x, y))
                ventana.blit(sprite_rotado, rect_rotado)
    
        # Dibujar rayo de aliento (fase 2 del combate)
        if self.rayo_aliento_activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_aliento <= 2000:  # Aparece durante 2s
    
                desplazamiento_x = 300  # Ajuste horizontal para que salga de la boca
                desplazamiento_y = 90  # Ajuste vertical para mejor alineación
    
                # Posición de la boca del dragón
                if self.mirando_derecha:
                    boca_x = self.rect.right + desplazamiento_x + 120
                    angulo = 45  # Negativo para que apunte abajo a la derecha
                else:
                    boca_x = self.rect.left - desplazamiento_x - 25
                    angulo = -45   # Positivo para que apunte abajo a la izquierda
                
                boca_y = self.rect.top + desplazamiento_y + 10
                
                # Preparar sprite base
                sprite = self.sprite_rayo_escupido
                
                # Rotar primero a vertical
                sprite_vertical = pygame.transform.rotate(sprite, 90)
                
                # Escalar verticalmente (900 px de alto)
                sprite_escalado = pygame.transform.scale(sprite_vertical, (200, 900))
                
                # Rotar final según dirección sin invertir
                sprite_rotado = pygame.transform.rotate(sprite_escalado, angulo)
                
                # Obtener rectángulo con centro en la boca del dragón
                rect_rotado = sprite_rotado.get_rect(midtop=(boca_x, boca_y))
                
                # Dibujar
                self.sonido_aliento.play()
                ventana.blit(sprite_rotado, rect_rotado)
                


                
                # Ahora sí lo rotamos (45° o 135°)
                sprite_rotado = pygame.transform.rotate(sprite_escalado, angulo)
                
                # Posición desde la boca del dragón
                rect_rotado = sprite_rotado.get_rect(midtop=(boca_x, boca_y))
                ventana.blit(sprite_rotado, rect_rotado)
                
                if rect_rotado.colliderect(protagonista.rect):
                    if not protagonista.invulnerable:
                        protagonista.recibir_dano(self.dano_ataque)
                        protagonista.invulnerable = True
                        protagonista.tiempo_invulnerable = pygame.time.get_ticks()
                    
            else:
                self.rayo_aliento_activo = False
    



    def actualizar_combo_garras(self, protagonista):
        tiempo_actual = pygame.time.get_ticks()
        avance = 150
        delay = 275  # tiempo entre fases
    
        if self.fase_combo == -1:
            if tiempo_actual - self.tiempo_combo > 400:
                self.fase_combo = 0
                self.tiempo_combo = tiempo_actual
            return
    
        self.sprite_combo_disponible = True  # ← ACTIVAMOS visualización del combo
        self.sprite_idle_disponible = False
        self.sprite_cargando_rayo_disponible = False
        self.sprite_escupiendo_rayo_disponible = False
    
        if self.fase_combo == 0:
            self.rect.x += avance if self.mirando_derecha else -avance
            self.rect_ataque = pygame.Rect(
                self.rect.right if self.mirando_derecha else self.rect.left - 60,
                self.rect.top,
                60,
                self.rect.height
            )
            self.sprite_combo_fase = 0
            self.tiempo_hitbox_combo = tiempo_actual
    
            self.fase_combo = 1
            self.tiempo_combo = tiempo_actual
    
        elif self.fase_combo == 1 and tiempo_actual - self.tiempo_combo > delay:
            self.rect_ataque = None
            self.rect.x += avance if self.mirando_derecha else -avance
            self.rect_ataque = pygame.Rect(
                self.rect.right if self.mirando_derecha else self.rect.left - 60,
                self.rect.top,
                60,
                self.rect.height
            )
            self.sprite_combo_fase = 1
            self.tiempo_hitbox_combo = tiempo_actual
    
            self.fase_combo = 2
            self.tiempo_combo = tiempo_actual
    
        elif self.fase_combo == 2 and tiempo_actual - self.tiempo_combo > delay:
            self.rect_ataque = None
            self.rect.x += avance if self.mirando_derecha else -avance
            self.rect_ataque = pygame.Rect(
                self.rect.right - 70 if self.mirando_derecha else self.rect.left + 70,
                self.rect.top + self.rect.height*.35,
                100,
                self.rect.height *.5
            )
            self.sprite_combo_fase = 2
            self.tiempo_hitbox_combo = tiempo_actual
    
            self.fase_combo = 3
            self.tiempo_combo = tiempo_actual
    
        elif self.fase_combo == 3 and tiempo_actual - self.tiempo_combo > delay:
            self.rect_ataque = None
            self.sprite_combo_disponible = False  # ← APAGAMOS sprite combo
            self.sprite_combo_fase = None
            self.fase_combo = -1
            self.combo_activo = False
            self.atacando = False
            self.ataques_en_suelo = False
            self.iniciar_ataque_rayos(protagonista)
    
        # Desactivar la hitbox si ya pasó el tiempo
        if self.rect_ataque and tiempo_actual - self.tiempo_hitbox_combo > 200:
            self.rect_ataque = None
    
        
    def actualizar(self, protagonista, piso_y):
        """
        Esta función se ejecuta cada frame. Es el centro de control del dragón.
        Decide qué comportamiento actualizar: rayos, embestida, combo, física, etc.
        """
        if pygame.time.get_ticks() - self.ultimo_cambio_frame_teledirigido > 500:
            self.frame_actual_teledirigido = (self.frame_actual_teledirigido + 1) % len(self.sprites_teledirigidos)
            self.ultimo_cambio_frame_teledirigido = pygame.time.get_ticks()


        if self.fase_ataque_rayos != -1 and not self.rayo_escupido_activo:
            self.actualizar_ataque_rayos_en_vuelo(protagonista)
    
        elif self.atacando:
            if self.combo_activo:
                self.actualizar_combo_garras(protagonista)
            elif self.atque_embestida:
                self.actualizar_ataque_embestida(protagonista)
    
        else:
            # Gravedad si no está atacando
            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y
            if self.rect.y >= piso_y - self.rect.height:
                self.rect.y = piso_y - self.rect.height
                self.velocidad_y = 0
                self.en_suelo = True
            else:
                self.en_suelo = False
    
        # Actualiza rayos en movimiento
        self.actualizar_rayos(protagonista)

        #Rayo Fijo
        self.actualizar_rayo_fijo_ciclico(protagonista)

        # Duración del impacto en el suelo
        if self.impacto_suelo_activo:
            if pygame.time.get_ticks() - self.tiempo_impacto_suelo > 500:
                self.impacto_suelo_activo = False
                self.rect_impacto_suelo = None

    
        # Se acaba invulnerabilidad si ya pasó el tiempo
        if self.invulnerable and pygame.time.get_ticks() - self.tiempo_invulnerable > 250:
            self.invulnerable = False




    def recibir_dano(self, cantidad):
        if not self.invulnerable:
            self.vida_actual -= cantidad
            self.invulnerable = True
            self.tiempo_invulnerable = pygame.time.get_ticks()






    def dibujar(self, ventana, protagonista):
        self.dibujar_ataque_rayos(ventana, protagonista)
        self.dibujar_rayo_fijo(ventana, protagonista)
    
        if self.rayo_escupido_activo and not self.atacando and not self.combo_activo:
            self.dibujar_rayo_escupido(ventana, protagonista)
    
        vida_width = int(200 * (self.vida_actual / self.vida_max))
        pygame.draw.rect(ventana, (255, 0, 0), (self.ancho_ventana - 220, 20, 200, 20))
        pygame.draw.rect(ventana, (0, 255, 0), (self.ancho_ventana - 220, 20, vida_width, 20))
    
        # SPRITE RENDERING SEGÚN ESTADO
        if self.sprite_escupiendo_rayo_disponible:
            altura_extra = int(self.rect.height * 1.35)
            ancho = self.rect.width
            sprite_ajustado = pygame.transform.scale(self.sprite_escupiendo_rayo, (ancho * 1.35, altura_extra))
            sprite_ajustado = self.aplicar_filtro_dano(sprite_ajustado)
    
            rect_dibujo = sprite_ajustado.get_rect(midbottom=self.rect.midbottom)
            sprite_final = sprite_ajustado if self.mirando_derecha else pygame.transform.flip(sprite_ajustado, True, False)
            ventana.blit(sprite_final, rect_dibujo)
    
        elif self.sprite_embestida_ascendiendo_disponible:
            sprite = pygame.transform.scale(self.sprite_embestida_ascendiendo, (self.rect.width * 1.25, self.rect.height))
            sprite = self.aplicar_filtro_dano(sprite)
            sprite_final = sprite if self.mirando_derecha else pygame.transform.flip(sprite, True, False)
            ventana.blit(sprite_final, (self.rect.x, self.rect.y))
    
        elif self.sprite_embistiendo_disponible:
            sprite = pygame.transform.scale(self.sprite_embistiendo, (self.rect.width * 1.25, self.rect.height))
            sprite = self.aplicar_filtro_dano(sprite)
            sprite_final = sprite if self.mirando_derecha else pygame.transform.flip(sprite, True, False)
            ventana.blit(sprite_final, (self.rect.x, self.rect.y))
    
        elif self.sprite_ascendiendo_disponible:
            sprite = self.sprites_ascendiendo[self.frame_actual_ascenso]
            sprite = pygame.transform.scale(sprite, (int(self.rect.width * 0.75), int(self.rect.height * 1.4)))
            sprite = self.aplicar_filtro_dano(sprite)
            sprite_final = sprite if self.mirando_derecha else pygame.transform.flip(sprite, True, False)
            ventana.blit(sprite_final, self.rect)
    
        elif self.sprite_volando_horizontal_disponible:
            sprite = self.sprites_volando_horizontal[self.frame_actual_vuelo_horizontal]
            sprite = pygame.transform.scale(sprite, (int(self.rect.width * 1.25), self.rect.height))
            sprite = self.aplicar_filtro_dano(sprite)
            sprite_final = sprite if self.mirando_derecha else pygame.transform.flip(sprite, True, False)
            ventana.blit(sprite_final, (self.rect.x, self.rect.y))
    
        elif self.sprite_cargando_rayo_disponible:
            sprite = self.sprite_cargando_rayo
            sprite = pygame.transform.scale(sprite, (self.rect.width, self.rect.height))
            sprite = self.aplicar_filtro_dano(sprite)
            sprite_final = sprite if self.mirando_derecha else pygame.transform.flip(sprite, True, False)
            ventana.blit(sprite_final, self.rect)
    
        elif self.sprite_descendiendo_disponible:
            sprite = pygame.transform.scale(self.sprite_descendiendo, (int(self.rect.width * 1.35), int(self.rect.height * 1.3)))
            sprite = self.aplicar_filtro_dano(sprite)
            offset_y = int(self.ancho_dragon * 0.25)
            sprite_final = sprite if self.mirando_derecha else pygame.transform.flip(sprite, True, False)
            ventana.blit(sprite_final, (self.rect.x, self.rect.y - offset_y))
    
        elif self.sprite_combo_disponible:
            if self.sprite_combo_fase in [0, 1]:
                sprite = self.sprites_combo_garra[self.sprite_combo_fase]
                sprite = pygame.transform.scale(sprite, (self.rect.width, self.rect.height))
            elif self.sprite_combo_fase == 2:
                sprite = pygame.transform.scale(self.sprite_combo_mordida, (int(self.rect.width * 1.33), int(self.rect.height * 1.25)))
    
            sprite = self.aplicar_filtro_dano(sprite)
    
            if self.mirando_derecha:
                if self.sprite_combo_fase in [0, 1]:
                    ventana.blit(sprite, self.rect)
                else:
                    ventana.blit(sprite, (self.rect.x - self.ancho_dragon * 0.33, self.rect.y - self.altura_dragon * 0.25))
            else:
                sprite_flipped = pygame.transform.flip(sprite, True, False)
                if self.sprite_combo_fase in [0, 1]:
                    ventana.blit(sprite_flipped, self.rect)
                else:
                    ventana.blit(sprite_flipped, (self.rect.x + self.ancho_dragon * 0.33, self.rect.y - self.altura_dragon * 0.25))
    
        elif self.sprite_idle_disponible:
            sprite = pygame.transform.scale(self.sprite_idle, (self.rect.width, self.rect.height))
            sprite = self.aplicar_filtro_dano(sprite)
            sprite_final = sprite if self.mirando_derecha else pygame.transform.flip(sprite, True, False)
            ventana.blit(sprite_final, self.rect)
    
        else:
            self.sprite_idle_disponible = True
    
        # Impacto del suelo
        if self.impacto_suelo_activo and self.rect_impacto_suelo:
            # Escalamos el sprite al tamaño de la hitbox
            sprite_escalado = pygame.transform.scale(self.sprite_impacto_suelo, (self.rect_impacto_suelo.width, self.rect_impacto_suelo.height))
            
            # Centramos el sprite en la hitbox
            rect_dibujo = sprite_escalado.get_rect(center=self.rect_impacto_suelo.center)
            ventana.blit(sprite_escalado, rect_dibujo)
        
            # Daño al protagonista si colisiona
            if self.rect_impacto_suelo.colliderect(protagonista.rect):
                if not protagonista.invulnerable:
                    protagonista.recibir_dano(self.dano_ataque)
                    protagonista.invulnerable = True
                    protagonista.tiempo_invulnerable = pygame.time.get_ticks()

        
    


        if self.rect_ataque and self.combo_activo:
            escala_x = int(self.rect_ataque.width * 1.75)
            escala_y = int(self.rect_ataque.height)
        
            sprite_escalado = pygame.transform.scale(self.sprite_rayo_fisico, (escala_x, escala_y))
        
            # Calcular posición centrada sobre la hitbox
            rect_dibujo = sprite_escalado.get_rect(center=self.rect_ataque.center)
        
            if self.mirando_derecha:
                ventana.blit(sprite_escalado, rect_dibujo)
            else:
                sprite_volteado = pygame.transform.flip(sprite_escalado, True, False)
                ventana.blit(sprite_volteado, rect_dibujo)

        if self.rect_ataque and (self.fase_ataque == 2 or self.fase_ataque == 1) and self.atque_embestida:  # Fase 2 es cuando embiste
            escala_x = int(self.rect_ataque.width * 1.67)
            escala_y = int(self.rect_ataque.height * 1.67)
            
            if self.mirando_derecha:
                sprite_escalado = pygame.transform.scale(self.sprite_rayo_fisico, (escala_x, escala_y +37))
            else:
                sprite_escalado = pygame.transform.scale(self.sprite_rayo_fisico, (escala_x, escala_y +37))
        
            rect_dibujo = sprite_escalado.get_rect(center=self.rect_ataque.center)
        
            if self.mirando_derecha:
                ventana.blit(sprite_escalado, rect_dibujo)
            else:
                sprite_volteado = pygame.transform.flip(sprite_escalado, True, False)
                ventana.blit(sprite_volteado, rect_dibujo)


    
    
    def aplicar_filtro_dano(self, imagen):
        if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            copia = imagen.copy()
            filtro = pygame.Surface(imagen.get_size(), pygame.SRCALPHA)
            filtro.fill((255, 50, 50, 150))  # rojo con opacidad
            copia.blit(filtro, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            return copia
        return imagen

