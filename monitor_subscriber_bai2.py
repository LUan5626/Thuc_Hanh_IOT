import json
import os
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "iot/lab/sensor01/data"


def make_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Đã kết nối broker: {BROKER}:{PORT}")
    client.subscribe(TOPIC)
    print(f"Đang giám sát topic: {TOPIC} (Ctrl+C để dừng)\n")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))
    temp = data["temperature"]
    humi = data["humidity"]

    print(f"Device: {data['device_id']}")
    print(f"Temperature: {temp} C")
    print(f"Humidity: {humi} %")

    if temp > 35:
        print("CANH BAO: Nhiet do cao")
    if humi < 40:
        print("CANH BAO: Do am thap")
    print()


client = make_client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Đã dừng giám sát.")
    client.disconnect()