import json
import requests
import time
import threading
from action_song import Action
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
        self.control_start_playlist()
        print("starting")

    def control_start_playlist(self):
        try:
            query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            response = response.json()["items"]
            exists = False
            for v in response:
                if v["name"] == "Boombox Playlist":
                    exists = True
                    self.playlist_id = v["id"]
                    self.playlist_uri= v["uri"]
            if not exists:
                self.create_playlist()
        except:
            self.create_playlist()
    
    def get_status(self):
        #print("get_status")
        file = open("/home/pi/Desktop/Spotify/ECE4873/status.txt", "r+")  
        read = file.readline()
        file.close()
        return read
    
    def create_playlist(self):
        # Create a new playlist
        print("Trying to create playlist...")
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        
        request_body = json.dumps({
            "name": "Boombox Playlist", "description": "Songs from SMS", "public": True
        })
        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        response_json = response.json()
        self.playlist_id = response_json["id"]
        self.playlist_uri = response_json["uri"]
    

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
    def get_txt_songs_2(self, firstline):
   
        data = firstline.split("-")
        song_name = data[0]
        artist = data[1]

        song = self.get_spotify_uri(song_name, artist)
        #print(song)
        if(song == []): song = "cannot find song"
        else: print(song_name + " + "+ artist)
        return song 
       
    def add_song_to_playlist(self, firstline):
        print('add_song_to_playlist')
        song = self.get_txt_songs(firstline)
        print(song)
        if(song == "cannot find song"):return
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.playlist_id, song)
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        #print("added song is " + song[0])
        #print(response.json)
    
    def remove_song_from_playlist(self, firstline):
        song_2 = self.get_txt_songs_2(firstline)
        if(song_2 == "cannot find song"):return
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        request_body = json.dumps(
            { "tracks": [{"uri": "{}".format(song_2)}]})
        response = requests.delete(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        #print("removed song is " )
        #print(response.json)
        
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
            
            
