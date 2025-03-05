# Phát Hiện Và Đếm Phương Tiện Giao Thông

## Giới Thiệu
Dự án này triển khai hệ thống phát hiện và đếm phương tiện giao thông bằng YOLOv8 và PyQt5. Ứng dụng xử lý video đầu vào, phát hiện phương tiện và đếm số lượng xe khi chúng đi qua một đường cố định.

## Tính Năng
- **Phát hiện phương tiện theo thời gian thực** bằng YOLOv8.
- **Hệ thống đếm xe** khi phương tiện cắt ngang đường vạch kẻ.
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
├── README.md
├── requirements.txt
├── src/
|   └── model/
|   ├── yolo11n.pt
|   └── yolov8n.pt
│       ├── Thread_Capture.py            # Luồng đọc dữ liệu từ video hoặc camera
│       ├── Thread_Tracking.py        # Luồng xử lý phát hiện và đếm xe
│   ├── Thread_Stream.py            # Luồng xử lý việc stream video (hiển thị video hoặc gửi ra ngoài)
│   ├── config.py                # File chứa các đường link thư mục cần thiết (video, model)
│   ├── main.py                   # File chạy chương trình
│   ├── main_contronler.py        # File điều khiển logic chính

```

## Đa Luồng Với QThread
Ứng dụng sử dụng đa luồng (`QThread`) trong PyQt5 để đảm bảo hiệu suất cao và xử lý video mượt mà. Hệ thống bao gồm 3 luồng chính:

1. Luồng Thread_Capture:        Đọc video.
                                Lưu các frame vào Queue
2. Luồng Thread_Tracking:       Lấy các frame trong Queue
                               Xử lý Yolo, đếm xe
                               Vẽ lên frame rồi lưu lại vào Queue
4. Luồng Thread_Stream:         Lấy các frame trong Queue rồi hiển thị

Mô hình này giúp tối ưu hóa quá trình phát hiện và hiển thị hình ảnh mà không gây giật lag giao diện.

## Cấu Hình
- Thay đổi nguồn video hoặc đường dẫn mô hình trong `config.py`nếu cần

## Giấy Phép
Dự án này được cấp phép theo MIT License.
## Báo cáo
https://docs.google.com/document/d/1CEfRO2j_fvshY2qjRvJNXjiUDqIsq12YCrnuBMntJPo/edit?tab=t.0
