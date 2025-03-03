from PyQt5.QtCore import QThread, pyqtSignal
from detect import is_crossing_line, line_start, line_end

class CountingThread(QThread):
    vehicle_counted = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.counted_objects = set()

    def process_frame(self, results):
        vehicle_classes = [2, 3, 5, 7]  # Car, motorcycle, bus, truck
        new_count = 0

        for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
            x1, y1, x2, y2 = map(int, box[:4])
            class_id = int(cls)

            if class_id in vehicle_classes:
                obj_key = f"{x1}-{y1}-{x2}-{y2}"
                if obj_key not in self.counted_objects and is_crossing_line(x1, x2, y2, line_start, line_end):
                    self.counted_objects.add(obj_key)
                    new_count += 1

        self.vehicle_counted.emit(len(self.counted_objects))

    def stop(self):
        self.quit()
        self.wait()
