import cv2
from PyQt5.QtGui import QImage, QPixmap

line_start = (1500, 300)
line_end = (300, 720)

# Biến toàn cục để lưu số xe đếm được
counted_objects = set()

def is_crossing_line(x1, x2, y2, line_start, line_end):
    box_bottom_center = ((x1 + x2) // 2, y2)
    line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
    point_vec = (box_bottom_center[0] - line_start[0], box_bottom_center[1] - line_start[1])
    cross_product = line_vec[0] * point_vec[1] - line_vec[1] * point_vec[0]
    return abs(cross_product) < 5000

def draw_results(frame, results, fps):
    global counted_objects

    vehicle_classes = [2, 3, 5, 7]  # Car, motorcycle, bus, truck (COCO class IDs)

    cv2.line(frame, line_start, line_end, (0, 0, 255), 2)

    for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
        x1, y1, x2, y2 = map(int, box[:4])
        class_id = int(cls)

        if class_id in vehicle_classes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{results[0].names[class_id]}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Tạo định danh duy nhất cho object (dựa trên vị trí khung hình)
            obj_key = f"{x1}-{y1}-{x2}-{y2}"

            # Kiểm tra xem object có cắt qua line không và chưa được đếm
            if obj_key not in counted_objects and is_crossing_line(x1, x2, y2, line_start, line_end):
                counted_objects.add(obj_key)

    cv2.putText(frame, f"Vehicles Count: {len(counted_objects)}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return frame

def convert_cv2qt(frame):
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_image)
