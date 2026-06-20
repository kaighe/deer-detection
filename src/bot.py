import discord
import logging
import threading
import asyncio
import io
import time

logger = logging.getLogger("bot")

class DiscordBot(threading.Thread):
    def __init__(self, token: str, channel_id: int, daemon = None):
        super().__init__(daemon=daemon)

        self.token = token

        intents = discord.Intents.default()
        self.client = discord.Client(intents=intents)
        self.channel: discord.TextChannel = None
        self.ready = False

        @self.client.event
        async def on_ready():
            logger.info(f"Logged in as '{self.client.user.name}'")
            self.ready = True
            self.channel = self.client.get_channel(channel_id)

    def send(self, message: str, buffer:io.BytesIO=None, filename=None):
        if(self.channel == None): return

        file = None
        if(buffer != None):
            file = discord.File(fp=buffer, filename=filename)

        future = asyncio.run_coroutine_threadsafe(self.channel.send(message, file=file), self.client.loop)
        future.result()

    def run(self):
        while True:
            try:
                self.client.run(self.token, log_handler=None)
            except Exception as e:
                logger.exception(e)
                logger.info("Restarting in 5 seconds...")
                time.sleep(5)

if(__name__ == "__main__"):
    import os
    from dotenv import load_dotenv

    load_dotenv()

    bot = DiscordBot(
        token=os.getenv("DISCORD_TOKEN"),
        channel_id=int(os.getenv("DISCORD_CHANNEL")),
        daemon=True
    )

    bot.start()

    while(not bot.ready): pass

    while True:
        message = input(">>> ")
        bot.send(message)