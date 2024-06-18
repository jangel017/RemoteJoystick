import pygame
import json
import os
import time
from vgamepad import vgamepad

# Inicializar pygame
pygame.init()

# Definir el tamaño de la ventana
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Joystick Simulator')

# Crear una instancia de vgamepad
gamepad = vgamepad.VGamepad()

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
                key = data.get('key')
                
                # Ajusta los valores del joystick según la entrada del teclado
                if key == 'ArrowUp':
                    gamepad.press_button(vgamepad.button.UP)
                elif key == 'ArrowDown':
                    gamepad.press_button(vgamepad.button.DOWN)
                elif key == 'ArrowLeft':
                    gamepad.press_button(vgamepad.button.LEFT)
                elif key == 'ArrowRight':
                    gamepad.press_button(vgamepad.button.RIGHT)
                else:
                    # Liberar todos los botones si no se presiona ninguna tecla
                    gamepad.release_all_buttons()
            except json.JSONDecodeError:
                print("Error decoding JSON")
    else:
        print("JSON file not found")  # Agrega este mensaje de depuración si el archivo JSON no se encuentra
    
    # Limpiar la pantalla
    screen.fill(black)

    # Dibujar el joystick
    pygame.draw.circle(screen, red, (width // 2, height // 2), 15)

    # Actualizar la pantalla
    pygame.display.flip()

    # Ralentizar el bucle para no consumir toda la CPU
    time.sleep(0.1)

# Cerrar el gamepad al salir del bucle principal
gamepad.close()
