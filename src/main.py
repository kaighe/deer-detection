import os
from dotenv import load_dotenv
import time
import logging
from detector import Detector
from bot import DiscordBot

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="(%(asctime)s) [%(name)s] [%(levelname)s] -> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("main")

detector = Detector("model.pt")
bot = DiscordBot(
    token=os.getenv("DISCORD_TOKEN"),
    channel_id=int(os.getenv("DISCORD_CHANNEL")),
    daemon=True
)
bot.start()

watch_time = 0
last_message = 0
while True:
    detector.wait_for_motion(0.02)
    watch_time = time.perf_counter()
    while(time.perf_counter() - watch_time <= 5):
        results = detector.predict(threshold=0.5)
        for result in results:
            if(result.class_name in ["buck", "antlerless", "human"] and time.perf_counter() - last_message > 60*3):
                logger.info(f"Detected: {result.class_name}")
                buffer = detector.record(10, fps=5)
                buffer.seek(0)
                bot.send("DEER IN THE YARD, SHOOT HIS ASS", buffer=buffer, filename="capture.gif")
                last_message = time.perf_counter()