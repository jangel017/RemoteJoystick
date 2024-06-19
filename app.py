from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import uinput

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('joystick_data')
def handle_joystick_data(json):
    axes = json['axes']
    print('Received axes:', axes)

    # Map the axes to joystick axes
    axis_map = {
        0: uinput.ABS_X,
        1: uinput.ABS_Y,
        2: uinput.ABS_RX,
        3: uinput.ABS_RY
    }

    for i, axis_value in enumerate(axes):
        if i in axis_map:
            value = int(float(axis_value) * 32767)  # Scale to joystick range
            device.emit(axis_map[i], value)

if __name__ == '__main__':
    device = uinput.Device([
        uinput.ABS_X + (-32767, 32767, 0, 0),
        uinput.ABS_Y + (-32767, 32767, 0, 0),
        uinput.ABS_RX + (-32767, 32767, 0, 0),
        uinput.ABS_RY + (-32767, 32767, 0, 0)
    ])
    socketio.run(app, host='0.0.0.0', port=5353, debug=True)