import discord
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# There was an issue with CA issuing an incorrect cert
# re-download from https://crt.sh/?id=2835394

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        msg = message.content
        channel = message.channel

        # Handle -in command
        if ' in' and ' in ' not in msg and 'in' in msg:
            await channel.send(f'eyy I\'m {msg[msg.index('in'):]} here')

# If not hosted, load environment vars from .env file
# load_dotenv()

# Create discord client
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
client = MyClient()
client.run(DISCORD_TOKEN)
