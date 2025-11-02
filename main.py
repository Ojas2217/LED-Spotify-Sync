import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from colorthief import ColorThief
from urllib.request import urlopen
import io
from bleak import BleakClient
import asyncio

load_dotenv()
scope = "user-read-currently-playing user-read-playback-state"
auth_manager = SpotifyOAuth(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"),scope=scope,redirect_uri=os.getenv("REDIRECT_URI"))    
sp = spotipy.Spotify(auth_manager=auth_manager)
ADDRESS = os.getenv("LED_MAC_ADDRESS")
CHAR = os.getenv("LED_UUID")


def color(track):
    if(track['currently_playing_type']=="track"):
        cover = track['item']['album']['images'][-1]['url']
    else:   
        cover = track['item']['images'][-1]['url']        
    file = urlopen(cover)
    f = io.BytesIO(file.read())
    ct = ColorThief(f)
    dominant_color = ct.get_color(quality=1)

    return dominant_color

# Attempts to brighten high channels, and dim lower ones.
# Use this if you have cheap led's (like mine) which don't respond well to certain rgb combinations
def normalize(color):
    color = list(color)
    maxi = color.index(max(color))
    mini = color.index(min(color))
    r,g,b = color
    if(r==g==b):
        return color
    if(r==g):
        if(color[maxi]==r):
            return min(255,r+b),min(255,g+b),0
        else:
            return 0,0,min(255,b+r)
    if(g==b):
        if(color[maxi]==g):
            return 0,min(255,g+b),min(255,r+b)
        else:
            return min(255,r+b),0,0
    if(r==b):
        if(color[maxi]==r):
            return min(255,r+g),0,min(255,g+b)
        else:
            return 0,min(255,g+r),0
    else:
        color[maxi] = min(255,color[maxi]+color[mini])
        color[mini] = 0
        return color
    
async def change_led_color(color,track,client):
    r, g, b = normalize(color)
    print("Now Playing:", track['item']['name'],", Changing color to:",(r,g,b))
    data = bytes.fromhex(f"69960502{r:02X}{g:02X}{b:02X}FF") #BLE Command pattern: different string of bytes for different microcontrollers
    await client.write_gatt_char(CHAR, data,response=False)

async def LED():
    try:
        async with BleakClient(ADDRESS) as client:
            old_track_id = None
            while True:
                current_track = sp.current_playback()

                if(current_track['currently_playing_type']=="episode"):
                    episode = sp.current_playback(additional_types="episode")
                    current_track = episode

                current_track_id = current_track['item']['id']
                if(current_track_id != old_track_id):
                    clr = color(current_track)
                    await change_led_color(clr,current_track,client)
                    old_track_id = current_track_id
    except Exception as e:
        print("Unexpected error: ",e,"\nMake sure Spotify is open and No other device is connected to the LED's")

            
asyncio.run(LED())
