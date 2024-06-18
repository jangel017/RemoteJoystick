from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('joystick_data')
def handle_joystick_data(data):
    print('Received joystick data:', data)  # Imprime los datos recibidos en la consola del servidor
    with open('joystick_data.json', 'w') as f:
        json.dump(data, f)
    emit('response', {'status': 'received'})  # Responde al cliente

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)