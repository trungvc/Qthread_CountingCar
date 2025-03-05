from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import logging
from queue import Empty

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
class StreamThread(QThread):
    update_frame = pyqtSignal(object, object, float)

    def __init__(self, queue_stream):
        super().__init__()
        self.queue_stream = queue_stream
        self.running = True

    def run(self):
        while self.running:
            try:
                frame, results, fps = self.queue_stream.get(timeout=0.5)
                self.update_frame.emit(frame, results, fps)
            except Empty:
                continue

    def stop(self):
        self.running = False