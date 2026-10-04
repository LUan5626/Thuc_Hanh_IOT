import json
import os
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

status = "OFF"  # trạng thái ban đầu của đèn


def make_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def publish_status(client):
    payload = json.dumps({"device_id": "light01", "status": status})
    client.publish(STATUS_TOPIC, payload)
    print(f"Đã gửi trạng thái [{STATUS_TOPIC}]: {payload}")


def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Đã kết nối broker: {BROKER}:{PORT}")
    client.subscribe(CMD_TOPIC)
    print(f"Đang chờ lệnh tại topic: {CMD_TOPIC} (Ctrl+C để dừng)")


def on_message(client, userdata, msg):
    global status
    cmd = msg.payload.decode("utf-8").strip().upper()
    print(f"Nhận lệnh: {cmd}")
    if cmd == "ON" or cmd == "OFF":
        status = cmd
        publish_status(client)  # gửi trạng thái mới sau mỗi lệnh hợp lệ


client = make_client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Đã dừng thiết bị.")
    client.disconnect()