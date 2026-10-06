# Thực hành lập trình Python với giao thức MQTT

## Thành viên nhóm

| Họ tên | Mã sinh viên | Lớp |
|---|---|---|
| Nguyễn Khả Luận | B23DCCN514 | D23CNPM05 |
| Hoàng Trung Kiên | B23DCCN458 | D23CNPM05 |
| Trịnh Đức Mạnh | B23DCCN534 | D23CNPM05 |

## Cấu trúc thư mục

```
Thuc_Hanh_IOT/
├── publisher_bai1.py
├── subscriber_bai1.py
├── sensor_publisher_bai2.py
├── monitor_subscriber_bai2.py
├── device_bai3.py
├── controller_bai3.py
└── README.md
```

## Broker sử dụng

Mặc định dùng broker công cộng **HiveMQ**:

- Host: `broker.hivemq.com`
- Port: `1883`

Không cần cài đặt hay cấu hình gì thêm, chỉ cần máy có kết nối Internet.

> Lưu ý: broker công cộng ai cũng đọc và gửi được trên cùng topic, nên nếu thấy tin nhắn lạ lẫn vào kết quả thì chuyển sang Mosquitto local.

## Yêu cầu môi trường

- Python 3.x
- Thư viện `paho-mqtt` (code chạy được với cả bản 1.x và 2.x)

```
pip install paho-mqtt
```

## Cách chạy

Mở terminal tại thư mục gốc của repo (`Thuc_Hanh_IOT`). Mỗi chương trình chạy trong một terminal riêng. Luôn chạy phía **nhận** (subscriber, monitor, device) **trước**, phía **gửi** sau. Bấm `Ctrl+C` để dừng chương trình chạy liên tục.

### Bài 1: Gửi và nhận thông điệp cơ bản

Topic: `iot/lab/message`

```
python subscriber_bai1.py
python publisher_bai1.py
```

- `publisher_bai1.py` gửi 3 thông điệp, mỗi thông điệp gồm lời chào, mã sinh viên và họ tên của một thành viên trong nhóm.
- `subscriber_bai1.py` chạy liên tục, mỗi khi nhận tin thì in ra Topic, Payload và Time.

Ví dụ kết quả ở subscriber:

```
Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN514 - Nguyễn Khả Luận
Time: 10:15:20
```

### Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm

Topic: `iot/lab/sensor01/data`

```
python monitor_subscriber_bai2.py
python sensor_publisher_bai2.py
```

- `sensor_publisher_bai2.py` gửi dữ liệu mỗi 3 giây, payload dạng JSON:
  ```json
  {"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}
  ```
  Nhiệt độ sinh ngẫu nhiên trong khoảng 25 đến 40 °C, độ ẩm trong khoảng 30 đến 80 %.
- `monitor_subscriber_bai2.py` in dữ liệu nhận được và cảnh báo:
  - Nhiệt độ > 35 °C: `CANH BAO: Nhiet do cao`
  - Độ ẩm < 40 %: `CANH BAO: Do am thap`

Ví dụ kết quả ở monitor:

```
Device: sensor01
Temperature: 36.1 C
Humidity: 38.7 %
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

### Bài 3: Điều khiển đèn thông minh

Topic: `iot/lab/light01/cmd` (lệnh) và `iot/lab/light01/status` (trạng thái)

```
python device_bai3.py
python controller_bai3.py
```

- `device_bai3.py` (đèn) subscribe topic `cmd`. Nhận `ON` hoặc `OFF` thì đổi trạng thái và publish trạng thái mới lên topic `status`, dạng:
  ```json
  {"device_id": "light01", "status": "ON"}
  ```
  Lệnh không hợp lệ bị bỏ qua. Trạng thái ban đầu của đèn là `OFF`.
- `controller_bai3.py` cho nhập lệnh `ON` hoặc `OFF` từ bàn phím, publish lên topic `cmd`, đồng thời subscribe topic `status` để hiển thị trạng thái đèn. Bấm `Ctrl+C` để thoát.

Ví dụ kết quả ở controller:

```
Nhap lenh: ON
Da gui lenh ON toi light01

Trang thai nhan duoc:
{"device_id": "light01", "status": "ON"}
```

## Kết quả đạt được

- **Bài 1:** publisher gửi đúng topic, subscriber nhận đúng dữ liệu và hiển thị rõ Topic, Payload, Time. Subscriber chạy liên tục đến khi bấm Ctrl+C, publisher gửi nhiều thông điệp liên tiếp (mỗi thành viên một thông điệp).
- **Bài 2:** cảm biến gửi JSON tuần hoàn mỗi 3 giây, monitor phân tích được dữ liệu và cảnh báo đúng điều kiện ngưỡng.
- **Bài 3:** điều khiển được thiết bị qua MQTT, thiết bị phản hồi đúng trạng thái, giao tiếp hai chiều thông qua hai topic `cmd` và `status`.

## Mô hình tổ chức topic

Dữ liệu được tổ chức theo mô hình thiết bị, topic, payload:

| Thiết bị | Topic | Chiều | Payload |
|---|---|---|---|
| Thông điệp chung | `iot/lab/message` | publisher → subscriber | Chuỗi văn bản |
| sensor01 | `iot/lab/sensor01/data` | sensor → monitor | JSON nhiệt độ, độ ẩm |
| light01 | `iot/lab/light01/cmd` | controller → đèn | `ON` / `OFF` |
| light01 | `iot/lab/light01/status` | đèn → controller | JSON trạng thái |