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

        # Handle links in listen-to-this-song
        DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL')
        PLAYLIST_ID = os.getenv('PLAYLIST_ID')
        if message.channel.name == DISCORD_CHANNEL and 'open.spotify.com' in msg:
            print(f'Got message: {msg}')
            scope = 'playlist-modify-public'
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
            track = [msg]
            sp.playlist_add_items(PLAYLIST_ID, track)

        # Handle -in command
        if ' ' not in msg and msg[-2:] == 'in':
            await channel.send(f'eyy I\'m {msg} here')

# If not hosted, load environment vars from .env file
# load_dotenv()

# Create discord client
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
client = MyClient()
client.run(DISCORD_TOKEN)
