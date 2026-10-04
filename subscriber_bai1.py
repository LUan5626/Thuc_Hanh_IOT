import os
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "iot/lab/message"


def make_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Đã kết nối broker: {BROKER}:{PORT}")
    client.subscribe(TOPIC)
    print(f"Đang lắng nghe topic: {TOPIC} (Ctrl+C để dừng)\n")


def on_message(client, userdata, msg):
    print("Nhan duoc message:")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {msg.payload.decode('utf-8')}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")


client = make_client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Đã dừng subscriber.")
    client.disconnect()