import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO
from detect import draw_results

class VideoThread(QThread):
    # Phát tín hiệu frame và kết quả detection ra ngoài
    frame_ready = pyqtSignal(object, float)    # (frame, fps)
    results_ready = pyqtSignal(object)         # YOLO detection results

    def __init__(self, video_path='video.mp4', model_path='D:\\tt\\t1\\model\\yolov8n.pt'):
        super().__init__()
        self.video_path = video_path
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(self.video_path)
        self.running = True
        self.prev_time = time.time()

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            curr_time = time.time()
            fps = 1 / (curr_time - self.prev_time)
            self.prev_time = curr_time

            # Chạy YOLO detection
            results = self.model(frame)

            # Vẽ kết quả detection lên frame
            frame = draw_results(frame, results, fps)

            # Phát frame và results ra ngoài để các luồng khác xử lý
            self.frame_ready.emit(frame, fps)
            self.results_ready.emit(results)

        self.cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
