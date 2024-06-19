from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('simulate.html')

@socketio.on('joystick_data')
def handle_joystick_data(json):
    keys = json.get('keys')  # Obtener el valor de la clave 'keys' o None si no existe
    if keys is not None:
        # Procesar el valor de 'keys' si existe
        print("Valor de 'keys' recibido:", keys)
        # Aquí puedes agregar cualquier lógica adicional que necesites
    else:
        print("La clave 'keys' no está presente en el diccionario recibido:", json)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5353, debug=True)
