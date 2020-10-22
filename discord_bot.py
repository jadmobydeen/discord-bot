import discord
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# cert issue: https://crt.sh/?id=2835394

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL')
        PLAYLIST_ID = os.getenv('PLAYLIST_ID')
        msg = message.content
        channel = message.channel
        if message.channel.name == DISCORD_CHANNEL and 'open.spotify.com' in msg:
            print(f'Got message: {msg}')
            scope = 'playlist-modify-public'
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
            track = [link]
            sp.playlist_add_items(PLAYLIST_ID, track)

        if ' ' not in msg and msg[-2:] == 'in':
            await channel.send(f'eyy I\'m {msg} here')

# load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = MyClient()
client.run(DISCORD_TOKEN)
