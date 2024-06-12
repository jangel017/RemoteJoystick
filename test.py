from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('joystick_data')
def handle_joystick_data(json):
    print('Received joystick data:', json)  # Imprime los datos recibidos en la consola del servidor
    emit('response', {'status': 'received'})  # Responde al cliente

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)  # Ejecutar en modo depuración
