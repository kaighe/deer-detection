import cv2
import imageio
import io
import threading
import time
from collections import deque

class Camera(threading.Thread):
    def __init__(self, video:int=0, fps=5, size=(640, 640), capture_length=10.0, daemon=None):
        super().__init__(daemon=daemon)
        self.video = cv2.VideoCapture(video)

        self.fps = fps
        self.size = size
        self.capture_length = capture_length

        self.frames = deque(maxlen=round(capture_length*fps))
        self.new_frame = False

    def run(self):
        while True:
            start_time = time.perf_counter()

            check, frame = self.video.read()
            frame = cv2.resize(frame, self.size)
            self.frames.append(frame)
            self.new_frame = True

            time.sleep(max(0.0, 1/self.fps - (time.perf_counter() - start_time)))
    
    def frame(self, blocking=True):
        if(not blocking):
            return self.frames[0]
        else:
            while(not self.new_frame): pass
            self.new_frame = False
            return self.frames[0]
    
    def save(self):
        frames = self.frames.copy()
        buffer = io.BytesIO()
        imageio.mimsave(buffer, frames, format="GIF", duration=1/self.fps * 1000, loop=0)
        return buffer

if(__name__ == "__main__"):
    camera = Camera(daemon=True)
    camera.start()

    while True:
        input("Press enter to save gif.")
        camera.save("test.gif")