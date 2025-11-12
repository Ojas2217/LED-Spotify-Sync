# LED-Spotify-Sync
A simple python script that connects to your spotify, and changes the color of your LED lights to the color of the currently playing songs album cover.

The script fetches the currently playing song from the Spotify Web API, extracts the album art’s dominant color using colorThief, and sends a BLE color command to your LED controller.
## Configuration
Before you can actually run the script you need to configure a few environment variables found in the .env file
Instructions on how you can configure them are already in the file.

However, finding the BLE command pattern is a bit tricky, personally I used apple's packet logger tool, which allowed me to log packets sent from my iphone to the LED's microcontroller, then I analyzed the packets with wireshark which lead me to the pattern. But
there's also an android friendly approach, which I think is simpler and can be found [here](https://medium.com/propeller-health-tech-blog/bluetooth-le-packet-capture-on-android-a2109439b2a1)

I also left the pattern that i found in the .env file to give you an idea of what it's supposed to look like, but unless you have the exact same LED's that I do it most likely won't work.


## Installation & Usage
Make sure you have python installed and a venv setup.

Clone the repository

```
git clone https://github.com/Ojas2217/LED-Spotify-Sync.git
```

Install requirements

```
pip install -r requirements.txt
```

Navigate to the project and run main.py
```
python -u main.py
```

There's also a .ps1 script which you could move to your desktop to make the script more accessible.

