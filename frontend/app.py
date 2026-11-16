"""
Real-Time Web Dashboard Backend (Flask + MQTT Subscriber).
Subscribes to AWS IoT Core over TLS and serves live sensor telemetry to the browser UI.
"""
from collections import deque
import json
import os
import threading
import time

from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")
PORT = int(os.getenv("AWS_IOT_PORT", "8883"))
base_client = os.getenv("CLIENT_ID", "MyDemoDevice")
# Use a distinct Client ID for the dashboard subscriber so it doesn't kick off the publisher!
SUB_CLIENT_ID = os.getenv("DASHBOARD_CLIENT_ID", f"{base_client}-Dashboard")
TOPIC = os.getenv("TOPIC", "sensors/temperature")
CERT_DIR = os.getenv("CERT_DIR", "../certs")

CA_PATH = os.path.join(CERT_DIR, "AmazonRootCA1.pem")
CERT_PATH = os.path.join(CERT_DIR, "certificate.pem.crt")
KEY_PATH = os.path.join(CERT_DIR, "private.pem.key")

history = deque(maxlen=30)
mqtt_status = {"connected": False, "last_error": None, "endpoint": ENDPOINT, "topic": TOPIC}


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        mqtt_status["connected"] = False
        mqtt_status["last_error"] = str(reason_code)
        print(f"[Dashboard] MQTT Connection failed: {reason_code}", flush=True)
    else:
        mqtt_status["connected"] = True
        mqtt_status["last_error"] = None
        print(f"[Dashboard] Connected to AWS IoT as '{SUB_CLIENT_ID}', subscribing to '{TOPIC}'", flush=True)
        client.subscribe(TOPIC, qos=1)


def on_disconnect(client, userdata, flags, reason_code, properties):
    mqtt_status["connected"] = False
    print(f"[Dashboard] Disconnected ({reason_code})", flush=True)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        history.append(data)
        print(f"[Dashboard] Received telemetry: {data}", flush=True)
    except Exception as e:
        print(f"[Dashboard] Error parsing message: {e}", flush=True)


def start_mqtt_subscriber():
    if not ENDPOINT:
        mqtt_status["last_error"] = "AWS_IOT_ENDPOINT not set"
        return
    for p in (CA_PATH, CERT_PATH, KEY_PATH):
        if not os.path.isfile(p):
            mqtt_status["last_error"] = f"Missing cert: {p}"
            return

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=SUB_CLIENT_ID,
    )
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.tls_set(ca_certs=CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH)

    try:
        client.connect(ENDPOINT, PORT)
        client.loop_forever()
    except Exception as e:
        mqtt_status["last_error"] = str(e)
        print(f"[Dashboard] MQTT Exception: {e}", flush=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/telemetry")
def api_telemetry():
    return jsonify({
        "status": mqtt_status,
        "latest": history[-1] if history else None,
        "history": list(history)
    })


if __name__ == "__main__":
    t = threading.Thread(target=start_mqtt_subscriber, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=False)
