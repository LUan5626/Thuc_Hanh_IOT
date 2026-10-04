import os
import time
import paho.mqtt.client as mqtt

# MQTT Broker
BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))

TOPIC = "iot/lab/message"

MEMBERS = [
    {"ho_ten": "Nguyễn Khả Luận", "ma_sv": "B23DCCN514"},
    {"ho_ten": "Hoàng Trung Kiên", "ma_sv": "B23DCCN458"},
    {"ho_ten": "Trịnh Đức Mạnh", "ma_sv": "B23DCCN534"},
]


def make_client():
    """Tạo MQTT client (tương thích paho-mqtt 1.x và 2.x)."""
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def main():
    client = make_client()
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    print(f"Đã kết nối broker: {BROKER}:{PORT}")

    # Mỗi thành viên gửi một thông điệp
    for member in MEMBERS:
        payload = f"Xin chao tu client Python MQTT - {member['ma_sv']} - {member['ho_ten']}"
        info = client.publish(TOPIC, payload, qos=1)
        info.wait_for_publish()
        print(f"Đã gửi [{TOPIC}]: {payload}")
        time.sleep(1)

    client.loop_stop()
    client.disconnect()
    print("Đã hoàn thành gửi thông điệp.")


if __name__ == "__main__":
    main()