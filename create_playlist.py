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

class SpotifyManager:
    def __init__(self):
        self.user_id = spotify_user_id
        self.tracks = ""
        self.playlist_uri = ""
        self.playlist_id = ""
        self.spotify_token = Refresh().refresh()
        print("starting")

    

    def get_spotify_uri(self, song_name, artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        if(songs == []): uri = []
           
        # only use the first song
        else: uri = songs[0]["uri"]
        return uri
    
    # read a file for 'remove song'
    
    def get_device(self):
        query = "https://api.spotify.com/v1/me/player/devices"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json()
        
        #print(response_json["devices"])
    def get_song_info(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        variables = vars(response)
        #print(variables['status_code'])
        #response_json = response.json()
        if(variables['status_code'] == 200): return response.json()
        elif(variables['status_code'] == 204): return False
        #else: response_json = response.json()
        
        
    def get_playlist_info(self):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json() 
        # Album 
        #print(response_json)
        return(response_json)
        
    def get_playlist_item(self):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json() 
        # Album
        line = ""
        for index in range(len(response_json['items'])):
            song = response_json['items'][index]['track']['name']
            artist = response_json['items'][index]['track']['album']['artists'][0]['name']
            line += song + "-" + artist + "\n"
        return line   
            #print(response_json['items'][index]['track']['album']['name'])
        #print(line)  
    def find_location(self, firstline):
        target = 0
        song = self.get_txt_songs(firstline)
        curr = self.get_song_info()
        curr = curr['item']['uri']
        response_json = self.get_playlist_info()
       
        for index in range(len(response_json['items'])):
            all_song = response_json['items'][index]['track']['uri']
            if(song == all_song): target = index + 1
            if(curr == all_song): curr = index + 1
        
        output = str(target) + "/" + str(curr)
        return output
        #return line 
        # print(response.json())
         
songLength = 0
cp = SpotifyManager()

def updateLCDInfo():
    while True:
        global cp
        info = cp.get_song_info()
        if info and info['is_playing']:
            if (info['item']['name'] != lcd.songName):
                lcd.albumURL = info['item']['album']['images'][1]['url']
                lcd.songName = info['item']['name']
                lcd.artist = info['item']['artists'][0]['name']
                lcd.songLength = info['item']['duration_ms'] // 1000
                #time.sleep(.05)
                lcd.drawSongDetails()
            progress = info['progress_ms'] // 1000
            lcd.updateBar(progress/lcd.songLength)
        time.sleep(.5)    
            
if __name__ == '__main__':
    lcdThread = threading.Thread(target=updateLCDInfo)
    lcdThread.start()
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
            
            
