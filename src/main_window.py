from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from m1 import Ui_MainWindow
from video_thread import VideoThread
from counting_thread import CountingThread
from detect import convert_cv2qt
from PyQt5.QtWidgets import QApplication
import sys

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.video_thread = VideoThread('D:\\tt\\t1\data\\20240227_082854_054.MP4', 'model/yolov8n.pt')
        self.counting_thread = CountingThread()

        # Kết nối tín hiệu
        self.video_thread.frame_ready.connect(self.update_frame)
        self.video_thread.results_ready.connect(self.counting_thread.process_frame)
        self.counting_thread.vehicle_counted.connect(self.update_vehicle_count)

        self.video_thread.start()
        self.counting_thread.start()

    def update_frame(self, frame, fps):
        pixmap = convert_cv2qt(frame)
        self.ui.label.setPixmap(pixmap)
        self.ui.label.setScaledContents(True)

    def update_vehicle_count(self, count):
        self.ui.statusbar.showMessage(f"Total Vehicles: {count}")

    def show(self):
        self.main_win.show()

    def close(self):
        self.video_thread.stop()
        self.counting_thread.stop()
