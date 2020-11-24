import requests
import json
from refresh import Refresh
from secrets import spotify_token, spotify_user_id

class Spotify:

    def __init__(self):
        self.spotify_token = Refresh().refresh()
        self.user_id = spotify_user_id
        self.songAdded = False
        self.offset = 0
        self.playlist_uri = ""
        self.playlist_id = ""
        self.deviceId = ""
        self.getPlaylist()
        self.checkDevice()
        self.play_start()

    def checkDevice(self):
        query = "https://api.spotify.com/v1/me/player/devices"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        try:
            devices = response.json()["devices"]
            device = 0
            for i in devices:
                if i["name"][0:10] == "raspotify ":
                    device = i["id"]
                    self.deviceId = device
                    if (not i["is_active"]):
                        self.offset = 0
                        self.play_start()
                    break
        except:
            return False

    def getSongInfo(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        try:
            variables = vars(response)
            if(variables['status_code'] == 200):
                return response.json()
            elif(variables['status_code'] == 204):
                return False
        except:
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
        try:
            return response.json()['item']['album']['images'][1]['url']
        except:
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
        try:
            return response.json()['is_playing']
        except:
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
        try:
            return response.json()['item']['name']
        except:
            return False
        
    def getSongUri(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        try:
            return response.json()['item']['uri']
        except:
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
        try:
            return response.json()['item']['artists'][0]['name']
        except:
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
        try:
            return response.json()['item']['duration_ms'] // 1000
        except:
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
        response_json = 0
        try:
            response_json = response.json()["items"]
        except:
            return []
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
        try:
            self.playlist_uri = response_json["uri"]
            self.playlist_id = response_json["uri"].split(':')[2]
        except:
            return False
    
    def play_start(self):
        query = "https://api.spotify.com/v1/me/player/play?device_id={}".format(self.deviceId)
        request_body = json.dumps({
            "context_uri":"{}".format(self.playlist_uri),
            "offset":{"position":self.offset}})
        response = requests.put(
            query,
            data=request_body,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
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
        
    def pause(self):
        query = "https://api.spotify.com/v1/me/player/pause"
        request_body = json.dumps({"context_uri": "{}".format(self.playlist_uri)})
        response = requests.put(query, data=request_body,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        
    def nextSong(self):
        query = "https://api.spotify.com/v1/me/player/next"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        
    def prevSong(self):
        query = "https://api.spotify.com/v1/me/player/previous"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        
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
        try:
            response_json = response.json()["tracks"]["items"]
            if(len(response_json) == 0):
                return False
            song = response_json[0]["uri"]
            return song
        except:
            return False
    
    def addQueue(self, song):
        query = "https://api.spotify.com/v1/me/player/queue?uri={}".format(song)
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        
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
        self.songAdded = True
    

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

    def updateLocation(self):
        song_uri = self.getSongUri()
        if song_uri == False:
            self.offset = 0
            return
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = False
        try:
            response_json = response.json()["items"]
        except:
            return False
        j = 0
        for i in response_json:
            song = i["track"]["uri"]
            if song == song_uri:
                if j == 0 and self.offset > 0:
                    if self.songAdded:
                        self.offset = self.offset + 1
                        self.play_start()
                        self.songAdded = False
                elif self.offset != j:
                    self.offset = j
                break
            j = j + 1
