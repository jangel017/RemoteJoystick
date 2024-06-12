from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Variable para almacenar el estado del joystick
joystick_state = {
    'axes': [0, 0, 0, 0],  # Ejemplo con 4 ejes
    'buttons': [0] * 8  # Ejemplo con 8 botones
}

# Bloqueo para proteger el acceso concurrente a joystick_state
lock = threading.Lock()

@app.route('/update', methods=['POST'])
def update_joystick_state():
    global joystick_state
    data = request.json
    with lock:
        joystick_state = data
    print('Received joystick data:', data)
    return jsonify({'message': 'Joystick data received'}), 200

# Función que emula el joystick periódicamente
def emulate_joystick():
    while True:
        with lock:
            print('Current joystick state:', joystick_state)
            # Aquí puedes agregar la lógica para emular el joystick real
        time.sleep(1)  # Esperar 1 segundo antes de la siguiente emulación

# Iniciar el hilo de emulación del joystick
threading.Thread(target=emulate_joystick, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Escuchar en todas las interfaces de red
