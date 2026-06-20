import cv2
from ultralytics import YOLO
import time
import numpy as np
import imageio
import io

class Result:
    bbox: tuple[float, float, float, float]
    class_name: str
    confidence: float

class Detector:
    def __init__(self, model: str, video: int = 0):
        self.video = cv2.VideoCapture(video)
        self.model = YOLO(model, verbose=False)
    
    def motion(self, interval=0.25):
        frame_a = self.video.read()[1]
        time.sleep(interval)
        frame_b = self.video.read()[1]
        if(frame_a is None or frame_b is None): return 0

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
        frame = self.video.read()[1]
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
    
    def record(self, length: float, fps = 10):
        frames = []

        start_time = time.perf_counter()
        frame_timer = 0
        while(time.perf_counter() - start_time < length):
            if(time.perf_counter() - frame_timer < 1/fps): continue
            frame_timer = time.perf_counter()

            frame = self.video.read()[1]
            if(frame is None): continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(rgb_frame)

        buffer = io.BytesIO()
        imageio.mimsave(buffer, frames, format="GIF", duration=len(frames)/length, loop=0)
        return buffer