# Phát Hiện Và Đếm Phương Tiện Giao Thông

## Giới Thiệu
Dự án này triển khai hệ thống phát hiện và đếm phương tiện giao thông bằng YOLOv8 và PyQt5. Ứng dụng xử lý video đầu vào, phát hiện phương tiện và đếm số lượng xe khi chúng đi qua một đường cố định.

## Tính Năng
- **Phát hiện phương tiện theo thời gian thực** bằng YOLOv8.
- **Hệ thống đếm xe** khi phương tiện cắt ngang đường vạch kẻ.
- **Giao diện đồ họa (GUI)** được xây dựng bằng PyQt5.
- **Hỗ trợ đa luồng** giúp tối ưu hiệu suất.

## Cài Đặt
### Yêu Cầu
Đảm bảo bạn đã cài đặt Python 3. Sau đó, cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```
> *Lưu ý:* Dự án sử dụng PyQt5 và YOLOv8 của Ultralytics.

## Hướng Dẫn Sử Dụng
### 1. Chuyển đổi tệp giao diện (nếu có chỉnh sửa)
Nếu bạn sửa đổi giao diện, chạy lệnh sau:
```bash
python convert_uitopy.py
```

### 2. Chạy ứng dụng
Thực hiện lệnh sau để khởi chạy chương trình:
```bash
python main.py
```

## Cấu Trúc Dự Án
```
Qthread_CountingCar/
├── .idea/                  # Thư mục cấu hình của PyCharm IDE
├── __pycache__/            # Thư mục chứa các file bytecode đã biên dịch
├── data/                   # Thư mục chứa dữ liệu video đầu vào
├── model/                  # Thư mục chứa tệp trọng số của mô hình YOLOv8
├── src/                    # Thư mục chứa mã nguồn chính của dự án
│   ├── convert_uitopy.py   # Tập lệnh chuyển đổi tệp .ui thành mã Python
│   ├── counting_thread.py  # Xử lý logic đếm phương tiện
│   ├── detect.py           # Chứa các hàm phát hiện và trực quan hóa
│   ├── main.py             # Điểm bắt đầu của ứng dụng
│   ├── main_window.py      # Quản lý cửa sổ chính của ứng dụng
│   ├── m1.py               # Tệp giao diện người dùng được tạo tự động
│   ├── untitled.ui         # Tệp thiết kế giao diện ban đầu (PyQt Designer)
│   └── video_thread.py     # Xử lý video và thực hiện phát hiện YOLOv8
└── requirements.txt        # Danh sách các thư viện Python cần thiết

```

## Đa Luồng Với QThread
Ứng dụng sử dụng đa luồng (`QThread`) trong PyQt5 để đảm bảo hiệu suất cao và xử lý video mượt mà. Hệ thống bao gồm 3 luồng chính:

1. Luồng VideoThread(QThread):  Đọc video.
                                Chạy YOLO detect.
                                Phát frame_ready để gửi frame lên giao diện.
                                Phát results_ready gửi kết quả detect sang CountingThread.
2. Luồng CountingThread(QThread): Nhận kết quả phát hiện từ YOLO.
                                  Thực hiện đếm xe.
                                  Phát signal vehicle_counted cập nhật số lượng xe lên giao diện.
3. MainWindow: Giao diện chính, tạo luồng, kết nối signal, hiển thị kết quả.

Mô hình này giúp tối ưu hóa quá trình phát hiện và hiển thị hình ảnh mà không gây giật lag giao diện.

## Cấu Hình
- Thay đổi nguồn video hoặc đường dẫn mô hình trong `video_thread.py`:
```python
self.video_thread = VideoThread('duong_dan_video.mp4', 'duong_dan_model/yolov8n.pt')
```
- Điều chỉnh **tọa độ đường kiểm tra** để đếm xe đi qua trong `detect.py` nếu cần:
```python
line_start = (1500, 400)
line_end = (300, 720)
```

## Giấy Phép
Dự án này được cấp phép theo MIT License.
## Báo cáo
https://docs.google.com/document/d/1CEfRO2j_fvshY2qjRvJNXjiUDqIsq12YCrnuBMntJPo/edit?tab=t.0
