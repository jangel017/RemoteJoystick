from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import uinput

app = Flask(__name__)
socketio = SocketIO(app)

# Crear un joystick virtual con python-uinput
device = uinput.Device([
    uinput.BTN_JOYSTICK,
    uinput.ABS_X + (-100, 100, 0, 0),
    uinput.ABS_Y + (-100, 100, 0, 0)
])

@app.route('/')
def index():
    return render_template('simulate.html')

@socketio.on('joystick_data')
def handle_joystick_data(json_data):
    print('Received joystick data:', json_data)

    x_value = 0
    y_value = 0

    if 'ArrowUp' in json_data['keys']:
        y_value = -100
    elif 'ArrowDown' in json_data['keys']:
        y_value = 100
    if 'ArrowLeft' in json_data['keys']:
        x_value = -100
    elif 'ArrowRight' in json_data['keys']:
        x_value = 100

    device.emit(uinput.ABS_X, x_value, syn=False)
    device.emit(uinput.ABS_Y, y_value)
    device.emit(uinput.BTN_JOYSTICK, 1)

    emit('response', {'status': 'received'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
