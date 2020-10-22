import discord
import os
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# There was an issue with CA issuing an incorrect cert
# re-download from https://crt.sh/?id=2835394

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        # Read in ID of last message read
        try:
            with open('last_id.txt') as f:
                last_id = int(f.readline())
                found_id = False
        except FileNotFoundError:
            last_id = 0
            found_id = True

        # Get the last 100 messages in listn-to-this-song
        DISCORD_SERVER = os.getenv('DISCORD_SERVER')
        DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL')
        for guild in self.guilds:
            if guild.name == DISCORD_SERVER:
                break
        channel = discord.utils.get(guild.text_channels, name=DISCORD_CHANNEL)
        messages = await channel.history(limit=100).flatten()

        # Pull new Spotify links out of messages
        tracks = []
        for message in messages:
            link = message.content
            if message.id > last_id and ' ' not in link and 'open.spotify.com' in link:
                tracks.append(link)

        # Add to playlist
        if tracks:
            PLAYLIST_ID = os.getenv('PLAYLIST_ID')
            scope = 'playlist-modify-public'
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
            sp.playlist_add_items(PLAYLIST_ID, tracks)

            print('Added', len(tracks), 'tracks')

            # Update ID of last message read
            with open('last_id.txt', 'w') as f:
                f.write(str(messages[0].id))
        else:
            print('No new tracks to add')


# If not hosted, load environment vars from .env file
load_dotenv()

# Create discord client
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
client = MyClient()
client.run(DISCORD_TOKEN)
client.close()
