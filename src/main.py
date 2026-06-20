import os
from dotenv import load_dotenv
import time
import logging

from camera import Camera
from detector import Detector
from bot import DiscordBot
from webserver import WebServer

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="(%(asctime)s) [%(name)s] [%(levelname)s] -> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("main")

camera = Camera(fps=3, capture_length=10, daemon=True)
detector = Detector("model.pt", camera)
bot = DiscordBot(
    token=os.getenv("DISCORD_TOKEN"),
    channel_id=int(os.getenv("DISCORD_CHANNEL")),
    daemon=True
)
webserver = WebServer(camera, host="0.0.0.0", daemon=True)

camera.start()
bot.start()
webserver.start()

watch_time = 0
last_message = 0
while True:
    detector.wait_for_motion(0.02)
    watch_time = time.perf_counter()
    while(time.perf_counter() - watch_time <= 5):
        results = detector.predict(threshold=0.5)
        for result in results:
            if(result.class_name == "deer" and time.perf_counter() - last_message > 60*3):
                logger.info(f"Detected: {result.class_name}")
                time.sleep(camera.capture_length*0.75)
                buffer = camera.save()
                buffer.seek(0)
                bot.send("@everyone  |  **DEER IN THE YARD, SHOOT HIS ASS**", buffer=buffer, filename="capture.gif")
                last_message = time.perf_counter()