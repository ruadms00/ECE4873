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
    #data = s.recv(1024).decode()
    #print(data)
#     while(1):
#         #status = "Try"
#         #print(status)
#         #s.sendall(status.encode())
#         #c, addr = s.accept()
#         #change c to s
# 
#         time.sleep(1)
#         data = s.recv(1024, ).decode()
#         print(data)
#         f_data = data.split(":")
#         status = f_data[0]
# 
#         
#         if(status == "start"):
#             cp.control_start_playlist()
#             offset_shuffle = 1
#             offset = 1
#             status = status + "::: "
#         else:
#             a_song = Action(cp.playlist_uri, cp.spotify_token)
#             #status = cp.get_status()
#             if(status == "NULL"):
#                 status = status + ":::" + ""
#             elif(status == 'add'):
#                 firstline = f_data[1]
#                 
#                 firstline = firstline.replace("&", " ")
#                 print(firstline)
#                 cp.add_song_to_playlist(firstline) 
#                 queue = cp.get_playlist_item()
#                 if(queue != None):
#                     status = status + ":::" + queue
#                     
#             elif(status == "remove"):
#                 firstline = f_data[1]
#                 firstline = firstline.replace("&", " ")
#                 cp.remove_song_from_playlist(firstline)
#                 queue = cp.geret_playlist_item()
#                 status = status +":::"+ queue
#             elif(status == 'play'):
#                 if(offset == 1):
#                     info = cp.get_playlist_info()
#                     
#                     if(info['total']!= 0):
#                         active = a_song.play_1()
#                         #if(active):
#                         a_song.play_repeat()
#                         offset = 0
#                         #elif(active == False):
#                     else: error = 1
#                 elif(offset == 0):
#                     a_song.play_2()
#             elif(status == 'location'):
#                 status = status + ":::" + queue
#             elif(status == 'location' and offset == 0):
#                 firstline = f_data[1]
#                 firstline = firstline.replace("&", " ")
#                 #print(firstline)
#                 queue = cp.find_location(firstline)
#                 #print(queue)
#                 status = status + ":::" + queue
#             elif(status == 'pause'):
#                 a_song.pause()
#             elif(status== 'next'):
#                 a_song.skip_to_nextSong()
#             elif(status == 'prev'):
#                 a_song.skip_to_prevSong()
#            
#                 
#             #elif(status == 'info'): cp.get_song_info()
#             elif(status == 'shuffle'):
#                 if(offset_shuffle == 1):
#                      a_song.play_shuffle("true")
#                      offset_shuffle = 0
#                 elif(offset_shuffle == 0):
#                      a_song.play_shuffle("false")
#                      offset_shuffle = 1
#                 #file = open("/home/pi/Desktop/Spotify/ECE4873/status.txt",'w')
#                 #file.write("NULL
#         if(error == 0 and offset != 1 and (status != 'add' and status != 'remove' and status != 'location')):
#            
#             queue = cp.get_song_info()
#             if(queue != False):
#                 queue = queue['item']['album']['images'][0]['url']
#                 
#             else: queue = ""
#             status = status + ":::" + queue
#             #elif(queue == False): continue
#             
#             print(status)
#         
#         #status = "set as NULL"
#         #print(status)
#         s.send(status.encode())
#         #c.send(queue.encode())
#     #s.close()
#     s.close()
#     
            
            
