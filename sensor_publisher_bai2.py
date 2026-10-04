import json
import os
import random
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "iot/lab/sensor01/data"


def make_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


client = make_client()
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()
print(f"Đã kết nối broker: {BROKER}:{PORT}")

try:
    while True:
        data = {
            "device_id": "sensor01",
            "temperature": round(random.uniform(25, 40), 1),
            "humidity": round(random.uniform(30, 80), 1),
        }
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"Đã gửi [{TOPIC}]: {payload}")
        time.sleep(3)  # gửi mỗi 3 giây
except KeyboardInterrupt:
    print("Đã dừng cảm biến.")
    client.loop_stop()
    client.disconnect()