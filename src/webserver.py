import threading
from flask import Flask, render_template, send_file
import logging
import cv2
import io
import time
from camera import Camera

logging.getLogger("werkzeug").setLevel(logging.ERROR)

logger = logging.getLogger("webserver")

class WebServer(threading.Thread):
    def __init__(self, camera: Camera, host: str = "127.0.0.1", port: int = 5000, daemon = None):
        super().__init__(daemon=daemon)

        self.camera = camera
        self.host = host
        self.port = port

        self.app = Flask(
            __name__,
            static_folder="web/static",
            template_folder="web/templates"
        )

        self.app.add_url_rule("/", view_func=self.index)
        self.app.add_url_rule("/image", view_func=self.image)
    
    def run(self):
        while True:
            try:
                self.app.run(host=self.host, port=self.port)
            except Exception as e:
                logger.exception(e)
                logger.info("Restarting in 5 seconds...")
                time.sleep(5)
    
    def index(self):
        return render_template("index.html")
    
    def image(self):
        if(len(self.camera.frames) == 0): return "Camera not initialized.", 500
        frame = self.camera.frames[0].copy()
        success, buffer = cv2.imencode(".jpg", frame)
        if(not success): return "Could not encode image", 500

        return send_file(io.BytesIO(buffer.tobytes()), mimetype="image/jpeg")