import discord
import json
from core import file

# ========================
# Définition des variables
# ========================

CONFIG = file.json_read('config.json')
TOKEN = CONFIG['token']

# ===
# Bot
# ===
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
