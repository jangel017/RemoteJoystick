from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import uinput
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Crear el dispositivo uinput
device = uinput.Device([
    uinput.BTN_A,
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0)
])

# Posiciones actuales de los ejes
current_x = 127  # Valor medio para X (0-255)
current_y = 127  # Valor medio para Y (0-255)

# Parámetros de suavizado
smooth_factor = 0.1  # Cuanto más pequeño, más suave es el movimiento

@app.route('/')
def index():
    return render_template('simulate.html')

@socketio.on('joystick_data')
def handle_joystick_data(json):
    global current_x, current_y
    keys = json['keys']
    print('Received keys:', keys)
    
    # Map the key to joystick buttons
    event_map = {
        'ArrowUp': (-1, 0),
        'ArrowDown': (1, 0),
        'ArrowLeft': (0, -1),
        'ArrowRight': (0, 1),
        'a': 'BTN_A'
    }

    if 'a' in keys:
        device.emit(uinput.BTN_A, 1)  # Press
        device.emit(uinput.BTN_A, 0)  # Release
    
    if any(key in keys for key in event_map if key != 'a'):
        dx, dy = 0, 0
        for key in keys:
            if key in event_map and key != 'a':
                change_x, change_y = event_map[key]
                dx += change_x
                dy += change_y

        target_x = current_x + dx * 10
        target_y = current_y + dy * 10

        # Clamping the target position to [0, 255]
        target_x = max(0, min(255, target_x))
        target_y = max(0, min(255, target_y))

        # Interpolate towards the target position
        current_x += (target_x - current_x) * smooth_factor
        current_y += (target_y - current_y) * smooth_factor

        device.emit(uinput.ABS_X, int(current_x))
        device.emit(uinput.ABS_Y, int(current_y))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5353, debug=True)
