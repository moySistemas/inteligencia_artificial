import pygame
import random
import csv
import os
import pandas as pd







archivo_csv = open('datos_entrenamiento.csv', mode='a', newline='')
escribir_csv = csv.writer(archivo_csv)


if os.stat('datos_entrenamiento.csv').st_size == 0:
    escribir_csv.writerow([
        'nave_x', 'nave_y',
        'jugador_x', 'jugador_y',
        'bala1_x', 'bala1_y',
        'velocidad_bala1',
        'saltar',
        'colision_bala1',
        'bala2_x', 'bala2_y',
        'velocidad_bala2',
        'tecla_izquierda', 'tecla_ninguna', 'tecla_derecha'
    ])







# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w





#AGREGANDO LA BALA 2
# Variables para la bala 2 (caída vertical)
bala2 = pygame.Rect(random.randint(100, w - 100), -50, 16, 16)
velocidad_bala2 = random.randint(3, 7)
bala2_disparada = False


#Variables para el modo de juego 
mod_seleccionado = None







# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2
    global bala2, velocidad_bala2, bala2_disparada

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))




    # Bala 2 (vertical)
    if not bala2_disparada:
        velocidad_bala2 = random.randint(3, 7)
        bala2_disparada = True
    bala2.y += velocidad_bala2
    if bala2.y > h:
        # Reiniciar posición para que vuelva a caer
        bala2.y = -50
        bala2.x = jugador.x
        velocidad_bala2 = random.randint(3, 7)
    pantalla.blit(bala_img, (bala2.x, bala2.y))  # Puedes usar la misma imagen


    colision_bala1 = 0
    if jugador.colliderect(bala) or jugador.colliderect(bala2):
        print("Colisión detectada!")
        colision_bala1 = 1
        reiniciar_juego()



    #Imprimir valores en la pantalla
    texto_nave = fuente.render(f"Nave: (x={nave.x}, y={nave.y})", True, NEGRO)
    texto_jugador = fuente.render(f"Jugador: (x={jugador.x}, y={jugador.y})", True, NEGRO)
    texto_bala = fuente.render(f"Bala 1: (x={bala.x}, y={bala.y})", True, NEGRO)
    texto_vel = fuente.render(f"Velocidad Bala 1: {velocidad_bala}", True, NEGRO)
    texto_bala2 = fuente.render(f"Bala 2: (x={bala2.x}, y={bala2.y})", True, NEGRO)
    texto_vel2 = fuente.render(f"Velocidad Bala 2: {velocidad_bala2}", True, NEGRO)
        
    pantalla.blit(texto_nave, (10, 10))
    pantalla.blit(texto_jugador, (10, 35))
    pantalla.blit(texto_bala, (10, 60))
    pantalla.blit(texto_vel, (10, 85))
    pantalla.blit(texto_bala2,(10,135))
    pantalla.blit(texto_vel2,(10,160))


    saltar = 0
    if salto:
        texto_salto = fuente.render("¡Saltando!", True, NEGRO)
        pantalla.blit(texto_salto, (10, 110))  
        saltar = 1
    else:
        texto_salto = fuente.render("No saltando", True, NEGRO)
        pantalla.blit(texto_salto, (10, 110))  
        saltar = 0



    tecla_izq = 0
    tecla_no = 0
    tecla_der = 0

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        texto_direccion = fuente.render("Presionando: Derecha", True, NEGRO)
        pantalla.blit(texto_direccion, (10, 185))
        tecla_der = 1
    elif teclas[pygame.K_LEFT]:
        texto_direccion = fuente.render("Presionando: Izquierda", True, NEGRO)
        pantalla.blit(texto_direccion, (10, 185))
        tecla_izq = 1
    else:
        texto_direccion = fuente.render("No presiona Izq. ni Der.", True, NEGRO)
        pantalla.blit(texto_direccion, (10, 185))
        tecla_no = 1




    escribir_csv.writerow([
        nave.x, nave.y,
        jugador.x, jugador.y,
        bala.x, bala.y,
        velocidad_bala,
        saltar,
        colision_bala1,
        bala2.x,bala2.y,
        velocidad_bala2,
        tecla_izq,
        tecla_no,
        tecla_der,

        ])




# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))









# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, mod_seleccionado

    # Botones
    #boton_auto = pygame.Rect(w // 4, h // 2 - 60, 200, 50)
    #boton_manual = pygame.Rect(w // 4, h // 2, 200, 50)
    #boton_salir = pygame.Rect(w // 4, h // 2 + 60, 200, 50)

    ancho_boton = 200
    alto_boton = 50
    ancho_check = 30  
    alto_check = 30


    # Centrar los botones en la pantalla
    boton_auto = pygame.Rect((w - ancho_boton) // 2, (h - alto_boton) // 2 - 60, ancho_boton, alto_boton)
    boton_manual = pygame.Rect((w - ancho_boton) // 2, (h - alto_boton) // 2, ancho_boton, alto_boton)
    boton_salir = pygame.Rect((w - ancho_boton) // 2, (h - alto_boton) // 2 + 60, ancho_boton, alto_boton)
    #boton_extra = pygame.Rect(10, h - alto_boton - 10, ancho_boton, alto_boton)
    boton_extra = pygame.Rect(10, h - alto_boton - 10, 100, alto_boton)  
    boton_mod1 = pygame.Rect(boton_extra.right + 10, boton_extra.top, 100, alto_boton)
    boton_mod2 = pygame.Rect(boton_mod1.right + 10, boton_extra.top, 100, alto_boton)
    boton_mod3 = pygame.Rect(boton_mod2.right + 10, boton_extra.top, 100, alto_boton)
    boton_mod4 = pygame.Rect(boton_mod3.right + 10, boton_extra.top, 100, alto_boton)




    while menu_activo:
        pantalla.blit(fondo_img, (0, 0))

        # Dibujar botones
        pygame.draw.rect(pantalla, (0, 128, 255), boton_auto)
        pygame.draw.rect(pantalla, (0, 200, 100), boton_manual)
        pygame.draw.rect(pantalla, (200, 50, 50), boton_salir)
        pygame.draw.rect(pantalla, (50, 101, 221), boton_extra)
        #pygame.draw.rect(pantalla, (50, 101, 221), boton_mod1)
        #pygame.draw.rect(pantalla, (50, 101, 221), boton_mod2)
        #pygame.draw.rect(pantalla, (50, 101, 221), boton_mod3)
        #pygame.draw.rect(pantalla, (50, 101, 221), boton_mod4)

        #Definir colores de mod segun su estado
        COLOR_ACTIVO = (0, 200, 100)     
        COLOR_INACTIVO = (50, 101, 221)  
        color_mod1 = COLOR_ACTIVO if mod_seleccionado == "mod1" else COLOR_INACTIVO
        color_mod2 = COLOR_ACTIVO if mod_seleccionado == "mod2" else COLOR_INACTIVO
        color_mod3 = COLOR_ACTIVO if mod_seleccionado == "mod3" else COLOR_INACTIVO
        color_mod4 = COLOR_ACTIVO if mod_seleccionado == "mod4" else COLOR_INACTIVO
        pygame.draw.rect(pantalla, color_mod1, boton_mod1)
        pygame.draw.rect(pantalla, color_mod2, boton_mod2)
        pygame.draw.rect(pantalla, color_mod3, boton_mod3)
        pygame.draw.rect(pantalla, color_mod4, boton_mod4)





        # Dibujar texto sobre botones
        texto_a = fuente.render("Modo Auto", True, BLANCO)
        texto_m = fuente.render("Modo Manual", True, BLANCO)
        texto_q = fuente.render("Salir", True, BLANCO)
        texto_e = fuente.render("Data", True, BLANCO)
        texto_mod1 = fuente.render("Mod 1", True, BLANCO)
        texto_mod2 = fuente.render("Mod 2", True, BLANCO)
        texto_mod3 = fuente.render("Mod 3", True, BLANCO)
        texto_mod4 = fuente.render("Mod 4", True, BLANCO)





        pantalla.blit(texto_a, (boton_auto.x + 20, boton_auto.y + 10))
        pantalla.blit(texto_m, (boton_manual.x + 20, boton_manual.y + 10))
        pantalla.blit(texto_q, (boton_salir.x + 20, boton_salir.y + 10))
        pantalla.blit(texto_e, (boton_extra.x + 20, boton_extra.y + 10))
        pantalla.blit(texto_mod1, (boton_mod1.x + 20, boton_mod1.y + 10))
        pantalla.blit(texto_mod2, (boton_mod2.x + 20, boton_mod2.y + 10))
        pantalla.blit(texto_mod3, (boton_mod3.x + 20, boton_mod3.y + 10))
        pantalla.blit(texto_mod4, (boton_mod4.x + 20, boton_mod4.y + 10))

 


        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_auto.collidepoint(evento.pos):
                    if mod_seleccionado != None:
                        modo_auto = True
                        menu_activo = False
                    else:
                        print("Debes seleccionar un Mod antes de activar Modo Auto")
                       

                

                elif boton_manual.collidepoint(evento.pos):
                    modo_auto = False
                    menu_activo = False
                elif boton_salir.collidepoint(evento.pos):
                    #print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
                elif boton_extra.collidepoint(evento.pos):
                    print("Quieres usar el dataset pre-hecho")



                elif boton_mod1.collidepoint(evento.pos):
                    print("Mod 1 - Regresion Lineal")
                    mod_seleccionado = "mod1"
                    

                elif boton_mod2.collidepoint(evento.pos):
                    print("Mod 2 seleccionado")
                    mod_seleccionado = "mod2"

                    
                elif boton_mod3.collidepoint(evento.pos):
                    print("Mod 3 seleccionado")
                    mod_seleccionado = "mod3"
                    
                elif boton_mod4.collidepoint(evento.pos):
                    print("Mod 4 seleccionado")
                    mod_seleccionado = "mod4"




def mostrar_datos_csv():
    df = pd.read_csv('datos_entrenamiento.csv')
    print(df.sample(10))





# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    global bala2, bala2_disparada, velocidad_bala2
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_datos_csv()
    
    

    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

    # Reiniciar bala 2
    bala2.x = random.randint(100, w - 100)
    bala2.y = -50
    velocidad_bala2 = random.randint(3, 7)
    bala2_disparada = False

    #print("Datos recopilados para el modelo: ", datos_modelo)
    #mostrar_menu()




def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:



        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()


        teclas = pygame.key.get_pressed()

        if not pausa:



            if teclas[pygame.K_LEFT]:
                jugador.x -= 5  # Mover a la izquierda
            if teclas[pygame.K_RIGHT]:
                jugador.x += 5  # Mover a la derecha

            # Limitar el movimiento dentro de la pantalla
            if jugador.x < 0:
                jugador.x = 0
            if jugador.x > w - jugador.width:
                jugador.x = w - jugador.width





            
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            

            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()