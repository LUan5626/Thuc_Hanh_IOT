import os
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"


def make_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe(STATUS_TOPIC)


def on_message(client, userdata, msg):
    print("\nTrang thai nhan duoc:")
    print(msg.payload.decode("utf-8"))


client = make_client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()
time.sleep(1)  # chờ kết nối và subscribe xong

print("Nhập lệnh ON hoặc OFF (Ctrl+C để thoát)")
try:
    while True:
        cmd = input("Nhap lenh: ").strip().upper()
        client.publish(CMD_TOPIC, cmd)
        print(f"Da gui lenh {cmd} toi light01")
        time.sleep(0.5)  # chờ thiết bị phản hồi
except KeyboardInterrupt:
    print("\nĐã thoát controller.")
    client.loop_stop()
    client.disconnect()