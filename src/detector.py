import cv2
from ultralytics import YOLO
import time
import numpy as np
import io

from camera import Camera

class Result:
    bbox: tuple[float, float, float, float]
    class_name: str
    confidence: float

class Detector:
    def __init__(self, model: str, camera: Camera):
        self.model = YOLO(model, verbose=False)
        self.camera = camera
    
    def motion(self):
        self.camera.frame()
        if(len(self.camera.frames) < 2): return 0
        frame_a = self.camera.frames[1]
        frame_b = self.camera.frames[0]

        frame_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
        frame_a = cv2.GaussianBlur(frame_a, (21, 21), 0)
        frame_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
        frame_b = cv2.GaussianBlur(frame_b, (21, 21), 0)

        diff = cv2.absdiff(frame_a, frame_b)
        changes = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
        height, width = changes.shape

        motion = np.sum(changes) / (width*height) / 255

        return motion
    
    def wait_for_motion(self, threshold=0.02):
        while True:
            if(self.motion() > threshold): return

    def predict(self, threshold=0.0) -> list[Result]:
        frame = self.camera.frame()
        if(frame is None): return []

        results = []
        yolo_results = self.model.predict(frame, conf=threshold, verbose=False)
        for yolo_result in yolo_results:
            for box in yolo_result.boxes:
                result = Result()
                result.bbox = tuple(box.xyxy[0].tolist())
                result.confidence = box.conf[0].item()
                class_id = int(box.cls[0].item())
                result.class_name = yolo_result.names[class_id]
                
                results.append(result)
        return results