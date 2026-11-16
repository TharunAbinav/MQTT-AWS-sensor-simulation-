"""
Simulated IoT multi-sensor (temperature & humidity) that publishes to AWS IoT Core over MQTT + TLS.
"""
import json
import os
import random
import sys
import threading
import time

import paho.mqtt.client as mqtt

ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")
PORT = int(os.getenv("AWS_IOT_PORT", "8883"))
CLIENT_ID = os.getenv("CLIENT_ID", "MyDemoDevice")
TOPIC = os.getenv("TOPIC", "sensors/temperature")
INTERVAL = float(os.getenv("PUBLISH_INTERVAL", "5"))
CERT_DIR = os.getenv("CERT_DIR", "certs")

CA_PATH = os.path.join(CERT_DIR, "AmazonRootCA1.pem")
CERT_PATH = os.path.join(CERT_DIR, "certificate.pem.crt")
KEY_PATH = os.path.join(CERT_DIR, "private.pem.key")


def check_setup():
    if not ENDPOINT:
        sys.exit("ERROR: AWS_IOT_ENDPOINT is not set.")
    for path in (CA_PATH, CERT_PATH, KEY_PATH):
        if not os.path.isfile(path):
            sys.exit(f"ERROR: missing certificate file: {path}")


connected = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Connection failed: {reason_code}", flush=True)
    else:
        print(f"Connected to AWS IoT Core as '{CLIENT_ID}'", flush=True)
        connected.set()


def on_disconnect(client, userdata, flags, reason_code, properties):
    connected.clear()
    print(f"Disconnected ({reason_code}). Reconnecting...", flush=True)


def main():
    check_setup()

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID,
    )
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.tls_set(ca_certs=CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH)

    print(f"Connecting to {ENDPOINT}:{PORT} ...", flush=True)
    client.connect(ENDPOINT, PORT)
    client.loop_start()

    if not connected.wait(timeout=15):
        client.loop_stop()
        sys.exit("ERROR: could not connect within 15 seconds.")

    try:
        while True:
            payload = {
                "deviceId": CLIENT_ID,
                "temperature": round(20 + random.random() * 10, 2),
                "humidity": round(40 + random.random() * 40, 2),
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            info = client.publish(TOPIC, json.dumps(payload), qos=1)
            info.wait_for_publish(timeout=10)
            print("Published:", payload, flush=True)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Stopping...", flush=True)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
