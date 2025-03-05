import cv2
import time
import logging
import threading
from queue import Queue, Empty
from ultralytics import YOLO
from config import model_path
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
class ThreadTracking(threading.Thread):
    def __init__(self, input_queue, model_path=model_path, process_every_n_frames=1):
        super().__init__()
        self.model = YOLO(model_path)
        self.running = True
        self.input_queue = input_queue
        self.line_start = (1000, 300)
        self.line_end = (300, 720)
        self.output_queue = Queue()
        self.frame_counter = 0
        self.process_every_n_frames = process_every_n_frames
        self.counted_objects = set()
        self.total_vehicles = 0
        self.lock = threading.Lock()

    def run(self):
        while self.running:
            try:
                frame, fps = self.input_queue.get(timeout=0.5)
                self.frame_counter += 1

                if self.frame_counter % self.process_every_n_frames == 0:
                    results = self.model(frame)
                    self.process_results(frame, results)
                    frame = self.draw_results(frame, results, fps)
                    self.output_queue.put((frame, results, fps))
            except Empty:
                continue
            time.sleep(0.01)

    def process_results(self, frame, results):
        vehicle_classes = {2, 3, 5, 7}  # Car, motorcycle, bus, truck
        new_count = 0

        with self.lock:
            for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
                x1, y1, x2, y2 = map(int, box[:4])
                class_id = int(cls)

                if class_id in vehicle_classes:
                    obj_key = f"{x1}-{y1}-{x2}-{y2}"
                    if obj_key not in self.counted_objects and self.is_crossing_line(x1, y1, x2, y2):
                        self.counted_objects.add(obj_key)
                        new_count += 1
                        self.total_vehicles += 1  # Tăng tổng số xe đếm được

    def is_crossing_line(self, x1, y1, x2, y2):
        box_center = ((x1 + x2) // 2, (y1 + y2) // 2)
        x3, y3 = self.line_start
        x4, y4 = self.line_end

        line_vec = (x4 - x3, y4 - y3)
        point_vec = (box_center[0] - x3, box_center[1] - y3)
        cross_product = line_vec[0] * point_vec[1] - line_vec[1] * point_vec[0]

        return abs(cross_product) < 33000

    def draw_results(self, frame, results, fps):
        cv2.line(frame, self.line_start, self.line_end, (0, 0, 255), 2)

        for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
            x1, y1, x2, y2 = map(int, box[:4])
            class_id = int(cls)

            if class_id in {2, 3, 5, 7}:  # Car, motorcycle, bus, truck
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{results[0].names[class_id]}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                obj_key = f"{x1}-{y1}-{x2}-{y2}"
                if obj_key not in self.counted_objects and self.is_crossing_line(x1, y1, x2, y2):
                    self.counted_objects.add(obj_key)

        cv2.putText(frame, f"FPS: {fps:.2f}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Vehicles Count: {len(self.counted_objects)}", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return frame

    def output_stream(self):
        return self.output_queue

    def stop(self):
        self.running = False
        logging.info("[ThreadTracking] Dừng xử lý video.")