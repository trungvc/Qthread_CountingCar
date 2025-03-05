# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtWidgets import QMainWindow
# import cv2
# import logging
# from queue import Queue
# from gui.m1 import Ui_MainWindow
# from config import video_path, model_path
# from Thread_Stream import StreamThread
# from Thread_Capture import ThreadCapture
# from Thread_Tracking import ThreadTracking
# # Cấu hình logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)

#         self.capture_queue = Queue(maxsize=20)

#         self.capture = ThreadCapture(video_path, self.capture_queue)
#         self.Tracking_thread = ThreadTracking(self.capture_queue, model_path)
#         self.stream_thread = StreamThread(self.Tracking_thread.output_stream())  #
#         self.stream_thread.update_frame.connect(self.update_ui)

#         # Khởi động các luồng
#         self.capture.start()
#         self.Tracking_thread.start()
#         self.stream_thread.start()

#     # def update_ui(self, frame, results, fps):
#     #     frame = draw_results(frame, results, fps)  # Vẽ kết quả lên frame
#     #     pixmap = convert_cv2qt(frame)  # Chuyển đổi thành pixmap
#     #     self.ui.label.setPixmap(pixmap)
#     #     self.ui.label.setScaledContents(True)
#     #     self.ui.statusbar.showMessage(f"Tổng số phương tiện: {len(self.Tracking_thread.counted_objects)}")
#     def update_ui(self, frame):
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển thành RGB
#         height, width, channel = frame.shape
#         bytes_per_line = 3 * width
#         qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
#         pixmap = QPixmap.fromImage(qt_image)

#         self.ui.label.setPixmap(pixmap)
#         self.ui.label.setScaledContents(True)
#     def closeEvent(self, event):
#         # Dừng tất cả các luồng khi đóng ứng dụng
#         self.capture.stop()
#         self.Tracking_thread.stop()
#         self.stream_thread.stop()
#         event.accept()

import logging
from queue import Queue
from PyQt5.QtWidgets import QMainWindow
from config import video_path, model_path
from Thread_Stream import StreamThread
from Thread_Capture import ThreadCapture
from Thread_Tracking import ThreadTracking

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.capture_queue = Queue(maxsize=15)

        # Khởi tạo các luồng
        self.capture = ThreadCapture(video_path, self.capture_queue)
        self.Tracking_thread = ThreadTracking(self.capture_queue, model_path)
        self.stream_thread = StreamThread(self.Tracking_thread.output_stream())  # Sử dụng StreamThread mới

        # Khởi động luồng
        self.capture.start()
        self.Tracking_thread.start()
        self.stream_thread.start()

    def closeEvent(self, event):
        # Dừng tất cả các luồng khi đóng ứng dụng
        self.capture.stop()
        self.Tracking_thread.stop()
        self.stream_thread.stop()
        event.accept()
