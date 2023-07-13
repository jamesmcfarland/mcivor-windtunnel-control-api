from flask import Flask, request
from flask_cors import CORS
import serial
import serial.tools.list_ports
import atexit


# Function to detect the Arduino port
def detect_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description:
            return port.device
    return None


def send_control(sig, speed):
    global ard
    msg = f"<{sig}{speed}>"
    print("Sending:", msg)
    ard.write(msg.encode())


print("Starting...")

print("Detecting Arduino port...")
arduino_port = detect_arduino_port()
if arduino_port is None:
    print("Error: Arduino port not found.")
    exit()

print("Opening serial connection...")
ard = serial.Serial(arduino_port, 115200, timeout=0.5)

print("Starting Flask server...")
app = Flask(__name__)
print("Enabling CORS...")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

globalSpeed = 0
f1 = 0
f2 = 0
f3 = 0
f4 = 0

actual_globalSpeed = 0
actual_f1 = 0
actual_f2 = 0
actual_f3 = 0
actual_f4 = 0


@app.post("/setfans")
def hello_world():
    global globalSpeed
    global f1
    global f2
    global f3
    global f4

    json = request.get_json()
    newglobalSpeed = json["global"]
    newf1 = json["f1"]
    newf2 = json["f2"]
    newf3 = json["f3"]
    newf4 = json["f4"]

    if newglobalSpeed != globalSpeed:
        globalSpeed = newglobalSpeed
        send_control("0", globalSpeed)
    else:
        if newf1 != f1:
            send_control("1", f1)
        if newf2 != f2:
            send_control("2", f2)
        if newf3 != f3:
            send_control("3", f3)
        if newf4 != f4:
            send_control("4", f4)

    f1 = newf1
    f2 = newf2
    f3 = newf3
    f4 = newf4
    print(f"Global: {globalSpeed} F1: {f1} F2: {f2} F3: {f3} F4: {f4}")
    return f"Global: {globalSpeed} F1: {f1} F2: {f2} F3: {f3} F4: {f4}"


@app.get("/getfans")
def get_fans():
    global ard
    ard.reset_input_buffer()
    response = ard.readline().decode().strip()
    print("\nResponse:", response)
    response = response.split(" ")
    m1 = int(response[0]) / 255 * 100
    m2 = int(response[1]) / 255 * 100
    m3 = int(response[2]) / 255 * 100
    m4 = int(response[3]) / 255 * 100
    gbl = int(response[4]) / 255 * 100
    iteraton = response[5]
    print(
        f"m1: {response[0]} m2: {response[1]} m3: {response[2]} m4: {response[3]} global:{response[4]} iteration: {response[5]}\n"
    )
    return {
        "global": globalSpeed,
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "f4": f4,
        "actual_global": gbl,
        "actual_f1": m1,
        "actual_f2": m2,
        "actual_f3": m3,
        "actual_f4": m4,
    }


def onExit():
    print("\nClosing serial\nClosing server")
    ard.close()


atexit.register(onExit)

print("Server online and ready.")
