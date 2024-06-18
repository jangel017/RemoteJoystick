import pygame
import sys
import json
import os
import time

# Inicializar pygame
pygame.init()

# Definir el tamaño de la ventana
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Joystick Simulator')

# Definir los colores
black = (0, 0, 0)
red = (255, 0, 0)

# Definir la posición inicial del joystick
joystick_x = width // 2
joystick_y = height // 2

# Escalar las entradas del joystick de -100 a 100 a la resolución de la pantalla
def scale_input(value, max_screen_value):
    return int((value + 100) / 200 * max_screen_value)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Leer los datos del archivo JSON
    if os.path.exists('joystick_data.json'):
        with open('joystick_data.json', 'r') as f:
            try:
                data = json.load(f)
                print("Data from JSON:", data)  # Agrega este mensaje de depuración para ver qué datos se están leyendo
                key = data.get('key')
                
                # Ajusta los valores del joystick según la entrada del teclado
                if key == 'ArrowUp':
                    joystick_y = scale_input(-100, height)
                elif key == 'ArrowDown':
                    joystick_y = scale_input(100, height)
                elif key == 'ArrowLeft':
                    joystick_x = scale_input(-100, width)
                elif key == 'ArrowRight':
                    joystick_x = scale_input(100, width)
                else:
                    # Reset joystick to center if no key pressed
                    joystick_x = width // 2
                    joystick_y = height // 2
            except json.JSONDecodeError:
                print("Error decoding JSON")
    else:
        print("JSON file not found")  # Agrega este mensaje de depuración si el archivo JSON no se encuentra
    
    # Limpiar la pantalla
    screen.fill(black)

    # Dibujar el joystick
    pygame.draw.circle(screen, red, (joystick_x, joystick_y), 15)

    # Actualizar la pantalla
    pygame.display.flip()

    # Ralentizar el bucle para no consumir toda la CPU
    time.sleep(0.1)
