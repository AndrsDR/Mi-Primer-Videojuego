import pygame
import os

class Protagonista:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)  # Añade esto como primer línea
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.velocidad_y = 0
        self.velocidad_max = 10
        self.ease = .75
        self.saltando = False
        self.mirando_der = True
        self.atacando = False
        self.distancia_ataque = 50
        self.cont_izq = 0
        self.cont_der = 0
        self.relacion_suelo = 1
        self.rect_ataque = None
        self.tiempo_ataque = 0
        self.ultimo_ataque = 0

        self.vida = 100
        self.invulnerable = False
        self.tiempo_invulnerable = 1000
        self.dano = 5.5
        
        # Animación de correr
        self.cargar_animacion_correr()
        self.frame_actual_correr = 0
        self.tiempo_ultimo_frame = 0
        self.intervalo_frames = 160  # ms entre frames

        # Animación idle
        self.idle_frames_der = []
        self.idle_frames_izq = []
        self.frame_actual_idle = 0
        self.tiempo_ultimo_frame_idle = 0
        self.intervalo_idle = 400  # ms entre frames (más lento que correr)
        
        self.cargar_animaciones_idle()  # Nueva carga de animaciones

        # Sprite de ataque
        self.sprite_ataque_der = None
        self.sprite_ataque_izq = None
        self.cargar_sprite_ataque()

        self.sprint_disponible = True
        self.activar_sprint_value = False
        self.sprint_tiempo = 0
        self.ultima_vez_tiempo = 0
        self.duracion_sprint = 100  # Sprint dura 1s
        self.sprint_cooldown = 2000  # Espera 2s para poder usarlo otra vez
        self.sprint_alcance = 50
        self.velocidad_normal = self.velocidad_max
        
        # Constantes
        self.FUERZA_SALTO = -22
        self.GRAVEDAD = 2
        self.COOLDOWN_ATAQUE = 500
        self.DURACION_ATAQUE = .1

        self.sonido_ataque = pygame.mixer.Sound("Audio\Efecto de sonido\Efecto de sonido agitando espada.wav")



    def activar_sprint(self):
        if self.sprint_disponible:
            self.sprint_disponible = False
            self.activar_sprint_value = True
            self.sprint_tiempo = pygame.time.get_ticks()



    def sprint(self):
        if not self.activar_sprint_value:
            return
    
        tiempo_actual = pygame.time.get_ticks()
    
        # Acción del sprint
        self.velocidad_max = self.sprint_alcance
    
        # Finaliza el sprint
        if tiempo_actual - self.sprint_tiempo >= self.duracion_sprint:
            self.velocidad_max = self.velocidad_normal
            self.activar_sprint_value = False
            self.ultima_vez_tiempo = tiempo_actual  # inicia cooldown


    def actualizar_sprint_cooldown(self):
        if not self.sprint_disponible and not self.activar_sprint_value:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultima_vez_tiempo >= self.sprint_cooldown:
                self.sprint_disponible = True
    



    def recibir_dano(self, cantidad):
        if not self.invulnerable:
            self.vida -= cantidad
            self.invulnerable = True
            self.tiempo_invulnerable = pygame.time.get_ticks()


    def cargar_sprite_ataque(self):
        """Carga la imagen de ataque y crea versión espejo"""
        try:
            attack_path = os.path.join('IMG', 'attack.png')
            self.sprite_ataque_der = pygame.image.load(attack_path).convert_alpha()
            
            # Escala al tamaño adecuado (ajusta estos valores)
            ancho_ataque = self.ancho * .5
            alto_ataque = self.alto 
            self.sprite_ataque_der = pygame.transform.scale(
                self.sprite_ataque_der, 
                (int(ancho_ataque), int(alto_ataque))
            )
            
            # Versión invertida para ataque izquierdo
            self.sprite_ataque_izq = pygame.transform.flip(self.sprite_ataque_der, True, False)
            
        except Exception as e:

            # Placeholder de emergencia (mantén tu cuadrado rojo)
            self.sprite_ataque_der = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            self.sprite_ataque_der.fill((255, 0, 0, 128))
            self.sprite_ataque_izq = self.sprite_ataque_der

    def cargar_animaciones_idle(self):
        """Carga los frames de la animación idle"""
        try:
            carpeta_idle = os.path.join('IMG', 'Prota idle spritesheets')
            
            # Carga todos los frames ordenados
            archivos = sorted([f for f in os.listdir(carpeta_idle) 
            if f.startswith('frame_') and f.endswith('.png')])
            
            for archivo in archivos:
                frame = pygame.image.load(os.path.join(carpeta_idle, archivo)).convert_alpha()
                frame = pygame.transform.scale(frame, (self.ancho, self.alto))
                self.idle_frames_der.append(frame)
                self.idle_frames_izq.append(pygame.transform.flip(frame, True, False))
        
        except Exception as e:

            # Placeholder de emergencia
            placeholder = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            placeholder.fill((0, 0, 255, 128))  # Azul semitransparente
            self.idle_frames_der = [placeholder]
            self.idle_frames_izq = [placeholder]

    def actualizar_animacion_idle(self):
        """Actualiza los frames de la animación idle"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_frame_idle > self.intervalo_idle:
            self.frame_actual_idle = (self.frame_actual_idle + 1) % len(self.idle_frames_der)
            self.tiempo_ultimo_frame_idle = tiempo_actual

    def cargar_animacion_correr(self):
        try:
            self.correr_der_frames = []
            self.correr_izq_frames = []
            
            # Verifica la ruta exacta
            carpeta_sprites = os.path.join('IMG', 'Prota corriendo spritesheets')

            
            # Carga exactamente 6 frames (ajusta si son más)
            for i in range(1, 7):
                # Usa DOS guiones bajos (frame__)
                frame_path = os.path.join(carpeta_sprites, f'frame_{i}.png')
                
                if not os.path.exists(frame_path):
                    print(f"¡Archivo faltante: {frame_path}")
                    continue
                    
                frame = pygame.image.load(frame_path).convert_alpha()
                # Escala solo si es necesario
                if frame.get_size() != (self.ancho, self.alto):
                    frame = pygame.transform.scale(frame, (self.ancho, self.alto))
                
                self.correr_der_frames.append(frame)
                self.correr_izq_frames.append(pygame.transform.flip(frame, True, False))
            
            
            if len(self.correr_der_frames) == 0:
                raise Exception("No se cargaron frames válidos")
                
        except Exception as e:

            # Crea placeholder de emergencia
            placeholder = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            placeholder.fill((0, 255, 0, 128))  # Verde semitransparente para debug
            self.correr_der_frames = [placeholder]
            self.correr_izq_frames = [placeholder]


        
    def actualizar_animacion_correr(self):
        """Avanza al siguiente frame de animación cuando corresponde
    (se llama automáticamente desde mover_izquierda/derecha)"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_frame > self.intervalo_frames:
            self.frame_actual_correr = (self.frame_actual_correr + 1) % len(self.correr_der_frames)
            self.tiempo_ultimo_frame = tiempo_actual


    def dibujar_animacion_correr(self, ventana):
        """Dibuja el frame actual de la animación según la dirección
        (se llama automáticamente desde dibujar())"""
        if self.mirando_der:
            ventana.blit(self.correr_der_frames[self.frame_actual_correr], (self.x, self.y))
        else:
            ventana.blit(self.correr_izq_frames[self.frame_actual_correr], (self.x, self.y))


        
    def mover_izquierda(self, fps):
        if self.mirando_der == False and (self.atacando == False or self.saltando == True):
        
            self.cont_izq += 1
            pasos_totales = self.ease * fps
            progreso = self.cont_izq / pasos_totales
            
            if progreso < 0.1:
                self.x -= self.velocidad_max * 0.25
            elif progreso < 0.25:
                self.x -= self.velocidad_max * 0.5
            elif progreso < 0.5:
                self.x -= self.velocidad_max * 0.7
            else:
                self.x -= self.velocidad_max


            if self.atacando == False:
                self.actualizar_animacion_correr()
            else:
                self.actualizar_animacion_idle()
            
        if self.atacando == False:
            self.mirando_der = False
        # Añade esta línea al final:
    
    def mover_derecha(self, fps):

        if self.mirando_der == True and (self.atacando == False or self.saltando == True):
        
            self.cont_der += 1
            pasos_totales = self.ease * fps
            progreso = self.cont_der / pasos_totales
            
            if progreso < 0.1:
                self.x += self.velocidad_max * 0.25
            elif progreso < 0.25:
                self.x += self.velocidad_max * 0.5
            elif progreso < 0.5:
                self.x += self.velocidad_max * 0.7
            else:
                self.x += self.velocidad_max
            
        if self.atacando == False:
            self.mirando_der = True
        # Añade esta línea al final:
        self.actualizar_animacion_correr()  # <-- Actualiza la animación

    
    def saltar(self, piso_y):
        if not self.saltando and self.y >= piso_y - (self.alto * self.relacion_suelo):
            self.velocidad_y = self.FUERZA_SALTO
            self.saltando = True
    
    def atacar(self):
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.ultimo_ataque >= self.COOLDOWN_ATAQUE:
            self.sonido_ataque.play()
            # Calcula posición del ataque
            if self.saltando == False:
                self.cont_izq = 0  # Resetea contadores de movimiento
                self.cont_der = 0
            if self.mirando_der:
                self.rect_ataque = pygame.Rect(
                    self.x + self.ancho + self.distancia_ataque,  # Aparece a la derecha
                    self.y - 10,
                    self.sprite_ataque_der.get_width(),
                    self.sprite_ataque_der.get_height()
                )
                self.atacando = True
            else:
                self.rect_ataque = pygame.Rect(
                    self.x - self.sprite_ataque_izq.get_width() - self.distancia_ataque,  # Aparece a la izquierda
                    self.y - 10,
                    self.sprite_ataque_izq.get_width(),
                    self.sprite_ataque_izq.get_height()
                )
                self.atacando = True
            
            self.tiempo_ataque = tiempo_actual
            self.ultimo_ataque = tiempo_actual
            
        
    def actualizar_fisica(self, piso_y, ancho_ventana):
        self.rect.x = self.x
        self.rect.y = self.y

        self.y += self.velocidad_y
        self.velocidad_y += self.GRAVEDAD * 0.5
        
        if self.y >= piso_y - (self.alto * self.relacion_suelo):
            self.y = piso_y - (self.alto * self.relacion_suelo)
            self.velocidad_y = 0
            self.saltando = False

        # Limitar posición del protagonista dentro de la ventana
        if self.x <= 0:
            self.x = 0
        elif self.x >= ancho_ventana - self.rect.width:
            self.x = ancho_ventana - self.rect.width


    
    def dibujar(self, ventana):
        # Si está corriendo
        if self.cont_izq > 0 or self.cont_der > 0:
            if self.mirando_der:
                ventana.blit(self.correr_der_frames[self.frame_actual_correr], (self.x, self.y))
            else:
                ventana.blit(self.correr_izq_frames[self.frame_actual_correr], (self.x, self.y))
        else:
            # Animación idle
            self.actualizar_animacion_idle()
            if self.mirando_der:
                ventana.blit(self.idle_frames_der[self.frame_actual_idle], (self.x, self.y))
            else:
                ventana.blit(self.idle_frames_izq[self.frame_actual_idle], (self.x, self.y))

        # Dibujar ataque si está activo
        tiempo_actual = pygame.time.get_ticks()
        if self.rect_ataque and (tiempo_actual - self.tiempo_ataque) < self.DURACION_ATAQUE * 1000:
            if self.mirando_der:
                ventana.blit(self.sprite_ataque_der, 
                            (self.rect_ataque.x, self.rect_ataque.y))
            else:
                ventana.blit(self.sprite_ataque_izq, 
                            (self.rect_ataque.x, self.rect_ataque.y))
        else:
            self.rect_ataque = None
            self.atacando = False