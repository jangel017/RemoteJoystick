from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import uinput

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Create the uinput device
device = uinput.Device([
    uinput.BTN_A,
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0)
])

@app.route('/')
def index():
    return render_template('simulate.html')

@socketio.on('joystick_data')
def handle_joystick_data(json):
    keys = json.get('keys')  # Obtener el valor de la clave 'key' o None si no existe
    if keys is not None:
        # Procesar el valor de 'key' si existe
        print("Valor de 'keys' recibido:", keys)

        # Map the key to joystick buttons
        event_map = {
            'ArrowUp': uinput.ABS_Y,
            'ArrowDown': uinput.ABS_Y,
            'ArrowLeft': uinput.ABS_X,
            'ArrowRight': uinput.ABS_X,
            'a': uinput.BTN_A
        }

        if keys in event_map:
            device.emit(event_map[keys], 1)  # Press
            device.emit(event_map[keys], 0)  # Release
    else:
        print("La clave 'keys' no está presente en el diccionario recibido:", json)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5353, debug=True)
