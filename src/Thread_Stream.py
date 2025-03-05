# from PyQt5.QtCore import QTimer, QThread, pyqtSignal
# import logging
# from queue import Empty

# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# class StreamThread(QThread):
#     update_frame = pyqtSignal(object, object, float)

#     def __init__(self, queue_stream):
#         super().__init__()
#         self.queue_stream = queue_stream
#         self.running = True

#     def run(self):
#         while self.running:
#             try:
#                 frame, results, fps = self.queue_stream.get(timeout=0.5)
#                 self.update_frame.emit(frame, results, fps)
#             except Empty:
#                 continue

#     def stop(self):
#         self.running = False
import threading
import cv2
import time
import logging
from queue import Empty

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class StreamThread(threading.Thread):
    def __init__(self, queue_stream):
        super().__init__()
        self.queue_stream = queue_stream
        self.running = True

    def run(self):
        while self.running:
            try:
                frame, results, fps = self.queue_stream.get(timeout=0.5)
                self.display_frame(frame, results, fps)  # Hiển thị frame bằng OpenCV
            except Empty:
                continue
            time.sleep(0.01)

    def display_frame(self, frame, results, fps):
        """ Hiển thị frame bằng OpenCV """
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển thành RGB

        # Hiển thị thông tin lên frame
        # cv2.putText(frame, f"FPS: {fps:.2f}", (20, 50),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        # cv2.putText(frame, f"Vehicles Count: {len(results)}", (20, 100),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Hiển thị bằng OpenCV
        cv2.imshow("Vehicle Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Nhấn 'q' để thoát
            self.stop()

    def stop(self):
        self.running = False
        cv2.destroyAllWindows()  # Đóng cửa sổ khi dừng
