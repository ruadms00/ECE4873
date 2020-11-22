import requests
import json
from refresh import Refresh
from secrets import spotify_token, spotify_user_id

class Spotify:

    def __init__(self):
        self.spotify_token = Refresh().refresh()
        self.user_id = spotify_user_id
        self.playlist_uri = ""
        self.playlist_id = ""
        self.getPlaylist()
        self.setDevice()

    def setDevice(self):
        query = "https://api.spotify.com/v1/me/player/devices"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        devices = response.json()["devices"]
        device = 0
        for i in devices:
            if i["name"][0:9] == "raspotify":
                device = i["id"]
                break
        print(device)
        query = "https://api.spotify.com/v1/me/player/play"
        request_body = json.dumps({ "device_ids": ["{}".format(device)]})
        #request_body = json.dumps({"device_ids": "[{}]".format(device)})
        response = requests.put(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        print(response)

    def getSongInfo(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        variables = vars(response)
        if(variables['status_code'] == 200):
            return response.json()
        elif(variables['status_code'] == 204):
            return False

    def getArt(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        variables = vars(response)
        if(variables['status_code'] == 200):
            return response.json()['item']['album']['images'][1]['url']
        elif(variables['status_code'] == 204):
            return False
        
    def isPlaying(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        variables = vars(response)
        if(variables['status_code'] == 200):
            return response.json()['is_playing']
        elif(variables['status_code'] == 204):
            return False
        
    def getName(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        variables = vars(response)
        if(variables['status_code'] == 200):
            return response.json()['item']['name']
        elif(variables['status_code'] == 204):
            return False
        
    def getArtist(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        variables = vars(response)
        if(variables['status_code'] == 200):
            return response.json()['item']['artists'][0]['name']
        elif(variables['status_code'] == 204):
            return False
    
    def getLength(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        variables = vars(response)
        if(variables['status_code'] == 200):
            return response.json()['item']['duration_ms'] // 1000
        elif(variables['status_code'] == 204):
            return False
            
    def getQueue(self):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json()["items"]
        queue = []
        for i in response_json:
            song = i["track"]["name"]
            artist = i["track"]["artists"][0]["name"]
            queue.append(song + "::" + artist)
        return queue
        
    def getPlaylist(self):
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
                    self.playlist_uri= v["uri"]
                    self.playlist_id = v["uri"].split(':')[2]
                if not exists:
                    self.create_playlist()
        except:
            self.create_playlist()
    
    def create_playlist(self):
        # Create a new playlist
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        
        request_body = json.dumps({
            "name": "Boombox Playlist", "description": "Songs from SMS", "public": True
        })
        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        response_json = response.json()
        self.playlist_uri = response_json["uri"]
        self.playlist_id = response_json["uri"].split(':')[2]
    
    def play_start(self):
        query = "https://api.spotify.com/v1/me/player/play"
        request_body = json.dumps({"context_uri": "{}".format(self.playlist_uri)})
        response = requests.put(query, data=request_body,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        
    def play(self):
        query = "https://api.spotify.com/v1/me/player/play"
        response = requests.put(
            query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from actions_song 2")
        #print(response.json)
        
    def pause(self):
        query = "https://api.spotify.com/v1/me/player/pause"
        request_body = json.dumps({"context_uri": "{}".format(self.playlist_uri)})
        response = requests.put(query, data=request_body,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from actions_song")
        #print(response.json)
        
    def nextSong(self):
        query = "https://api.spotify.com/v1/me/player/next"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from skip_to_nextSong")
        #print(response.json)
        
    def prevSong(self):
        query = "https://api.spotify.com/v1/me/player/previous"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from skip_to_prevSong")
        #print(response.json)
        
    def shuffle(self):
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json()
        shuffle = response_json["shuffle_state"]
        query = "https://api.spotify.com/v1/me/player/shuffle?state={}".format(
            not shuffle)
        response = requests.put(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("play_shuffle")
        #print(response.json)
        
    def repeat(self):
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json()
        repeat = response_json["repeat_state"]
        if (repeat == "context"):
            repeat = "off"
        else:
            repeat = "context"
        query = "https://api.spotify.com/v1/me/player/repeat?state={}".format(
            repeat)
        response = requests.put(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        
    def formatSong(self, txt):
        data = txt.split("::")
        song_name = data[0]
        artist = data[1]
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
        song = response_json["tracks"]["items"][0]["uri"]
        return song 
    
    def add(self, song):
        song = self.formatSong(song)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.playlist_id, song)
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
    

    def remove(self, song):
        #this removes all of the same song, you could search for a specific song though
        song = self.formatSong(song)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        request_body = json.dumps(
            { "tracks": [{"uri": "{}".format(song)}]})
        response = requests.delete(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        
    def clear(self):
        query = "https://api.spotify.com/v1/playlists/{}/followers".format(
            self.playlist_id)
        response = requests.delete(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        self.create_playlist()
        
        
        
        
#     def find_location(self, firstline):
#         target = 0
#         song = self.get_txt_songs(firstline)
#         curr = self.get_song_info()
#         curr = curr['item']['uri']
#         response_json = self.get_playlist_info()
#        
#         for index in range(len(response_json['items'])):
#             all_song = response_json['items'][index]['track']['uri']
#             if(song == all_song): target = index + 1
#             if(curr == all_song): curr = index + 1
#         
#         output = str(target) + "/" + str(curr)
#         return output
        #return line 
        # print(response.json())
