from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta para actualizar el estado del joystick
@app.route('/update', methods=['POST'])
def update_joystick_state():
    data = request.json  # Obtener los datos enviados por el cliente
    print('Received joystick data:', data)  # Mostrar los datos recibidos en la consola del servidor
    # Aquí puedes agregar la lógica para emular el joystick, por ejemplo, enviar los datos a un joystick real o a un simulador
    return jsonify({'message': 'Joystick data received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)