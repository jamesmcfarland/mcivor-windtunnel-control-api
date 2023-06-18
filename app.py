from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
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
    globalSpeed = json["global"]
    f1 = json["f1"]
    f2 = json["f2"]
    f3 = json["f3"]
    f4 = json["f4"]
    print(f"Global: {globalSpeed} F1: {f1} F2: {f2} F3: {f3} F4: {f4}")
    return f"Global: {globalSpeed} F1: {f1} F2: {f2} F3: {f3} F4: {f4}"


@app.get("/getfans")
def get_fans():
    return {
        "global": globalSpeed,
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "f4": f4,
        "actual_global": actual_globalSpeed,
        "actual_f1": actual_f1,
        "actual_f2": actual_f2,
        "actual_f3": actual_f3,
        "actual_f4": actual_f4,
    }
