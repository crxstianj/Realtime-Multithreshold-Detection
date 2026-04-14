import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

zoom_factor = 1

detecciones = {
    "C1":  {"lower1": (0,   70, 50),  "upper1": (10,  255, 255),
                   "lower2": (170, 70, 50),  "upper2": (180, 255, 255),
                   "color":  (0, 0, 255)},
    "C2":  {"lower1": (5,   50, 20),  "upper1": (25,  200, 120),
                   "lower2": None,           "upper2": None,
                   "color":  (0, 140, 255)},
    "C3":    {"lower1": (100, 70, 50),  "upper1": (130, 255, 255),
                   "lower2": None,           "upper2": None,
                   "color":  (255, 0, 0)},
}

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        frame = np.asanyarray(color_frame.get_data())

        h, w, _ = frame.shape
        new_w = int(w / zoom_factor)
        new_h = int(h / zoom_factor)
        x1 = w // 2 - new_w // 2
        y1 = h // 2 - new_h // 2
        roi = frame[y1:y1+new_h, x1:x1+new_w]
        zoomed = cv2.resize(roi, (w, h), interpolation=cv2.INTER_LINEAR)

        hsv = cv2.cvtColor(zoomed, cv2.COLOR_BGR2HSV)
        display = zoomed.copy()

        for nombre, cfg in detecciones.items():
            mask = cv2.inRange(hsv, cfg["lower1"], cfg["upper1"])
            if cfg["lower2"] is not None:
                mask |= cv2.inRange(hsv, cfg["lower2"], cfg["upper2"])

            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornos = [c for c in contornos if cv2.contourArea(c) >= 5000]
            if not contornos:
                continue
            cnt = max(contornos, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(cnt)
            cv2.rectangle(display, (bx, by), (bx + bw, by + bh), cfg["color"], 2)
            cv2.putText(display, nombre, (bx, by - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, cfg["color"], 1)

        cv2.imshow("Deteccion HSV", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()