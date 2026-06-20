import cv2
import imageio
import io
import threading
import time
import logging
from collections import deque

logger = logging.getLogger("camera")

class Camera(threading.Thread):
    def __init__(self, video:int=0, fps=5, size=(640, 640), capture_length=10.0, daemon=None):
        super().__init__(daemon=daemon)
        self.video = cv2.VideoCapture(video)

        self.fps = fps
        self.size = size
        self.capture_length = capture_length

        self.frames: deque[cv2.typing.MatLike] = deque(maxlen=round(capture_length*fps))
        self.new_frame = False

    def run(self):
        while True:
            try:
                start_time = time.perf_counter()

                check, frame = self.video.read()
                frame = cv2.resize(frame, self.size)
                self.frames.appendleft(frame)
                self.new_frame = True

                time.sleep(max(0.0, 1/self.fps - (time.perf_counter() - start_time)))
            except Exception as e:
                logger.exception(e)
                logger.info("Restarting in 5 seconds...")
                time.sleep(5)
    
    def frame(self, blocking=True):
        if(not blocking):
            if(len(self.frames) == 0): return None
            return self.frames[0]
        else:
            while(not self.new_frame): pass
            self.new_frame = False
            return self.frames[0]
    
    def save(self):
        frames = self.frames.copy()
        frames = [cv2.cvtColor(x, cv2.COLOR_BGR2RGB) for x in frames]
        buffer = io.BytesIO()
        imageio.mimsave(buffer, frames[::-1], format="GIF", duration=1/self.fps * 1000, loop=0)
        return buffer

if(__name__ == "__main__"):
    camera = Camera(daemon=True)
    camera.start()

    while True:
        cv2.imshow("preview", camera.frame())
        cv2.waitKey(200)