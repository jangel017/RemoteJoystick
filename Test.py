from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import asyncio
from mavsdk import System

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

drone = System()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('joystick_data')
def handle_joystick_data(json):
    axes = json['axes']
    print('Received axes:', axes)
    asyncio.run(set_manual_control(axes))

async def set_manual_control(axes):
    roll = float(axes[0])
    pitch = float(axes[1])
    throttle = float(axes[2]) * 0.5 + 0.5  # Escala de -1 a 1 a 0 a 1
    yaw = float(axes[3])

    await drone.manual_control.set_manual_control_input(pitch, roll, throttle, yaw)

async def init_drone():
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    print("-- Starting manual control")
    await drone.manual_control.start_position_control()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_drone())
    socketio.run(app, host='0.0.0.0', port=5353, debug=True)
