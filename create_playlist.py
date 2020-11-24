import json
import requests
import time
import threading
from SpotifyAction import Spotify
from refresh import Refresh
from LCDControl import LCD
from secrets import spotify_token, spotify_user_id

offset = 1
error = 0
offset_shuffle = 1
queue = " "
lcd = LCD()
image = "sdf"
    
songLength = 0
spotify = Spotify()

def updateLCDInfo():
    while True:
        global spotify
        song = spotify.getSongInfo()
        if song and song['is_playing']:
            if (song['item']['name'] != lcd.songName):
                lcd.albumURL = song['item']['album']['images'][1]['url']
                lcd.songName = song['item']['name']
                lcd.artist = song['item']['artists'][0]['name']
                lcd.songLength = song['item']['duration_ms'] // 1000
                lcd.drawSongDetails()
            progress = song['progress_ms'] // 1000
            lcd.updateBar(progress/lcd.songLength)
        time.sleep(.5) 
            

if __name__ == '__main__':
    lcdThread = threading.Thread(target=updateLCDInfo)
    lcdThread.start()
    while True:
        cmd = lcd.getData()
        if cmd == 1:
            spotify.prevSong()
            time.sleep(1)
        elif cmd == 2:
            spotify.play()
            time.sleep(1)
        elif cmd == 3:
            spotify.pause()
            time.sleep(1)
        elif cmd == 4:
            spotify.nextSong()
            time.sleep(1)
        time.sleep(.001)
    